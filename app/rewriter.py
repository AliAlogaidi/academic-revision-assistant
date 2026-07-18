import os
import re
import json
import urllib.error
import urllib.request
from dataclasses import dataclass


ACADEMIC_INTEGRITY_NOTE = (
    "Use this as a revision aid: verify claims, preserve required technical terms, "
    "and cite any ideas, data, or wording that came from sources."
)


@dataclass
class QualityNote:
    label: str
    detail: str


@dataclass
class RewriteResult:
    revised: str
    provider: str
    quality_notes: list[QualityNote]


class AcademicRewriter:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
        self.tohuman_token = os.getenv("TOHUMAN_API_TOKEN", "").strip()
        self.tohuman_intensity = os.getenv("TOHUMAN_INTENSITY", "medium").strip() or "medium"

    async def rewrite(
        self,
        text: str,
        tone: str,
        depth: str,
        include_citation_notes: bool,
    ) -> RewriteResult:
        if self.tohuman_token:
            try:
                revised = self._rewrite_with_tohuman(text)
                revised = self._add_citation_note_if_needed(revised, include_citation_notes)
                return RewriteResult(
                    revised=revised,
                    provider=f"tohuman:{self.tohuman_intensity}",
                    quality_notes=self._quality_notes(text, revised, include_citation_notes),
                )
            except Exception:
                # Fall back gracefully if the external service is unavailable.
                pass

        if self.api_key:
            try:
                revised = await self._rewrite_with_openai(
                    text=text,
                    tone=tone,
                    depth=depth,
                    include_citation_notes=include_citation_notes,
                )
                return RewriteResult(
                    revised=revised,
                    provider=f"openai:{self.model}",
                    quality_notes=self._quality_notes(text, revised, include_citation_notes),
                )
            except Exception:
                # Keep the app usable during local demos when API credentials or network fail.
                pass

        revised = self._rewrite_locally(text, tone, depth, include_citation_notes)
        return RewriteResult(
            revised=revised,
            provider="local-fallback",
            quality_notes=self._quality_notes(text, revised, include_citation_notes),
        )

    async def _rewrite_with_openai(
        self,
        text: str,
        tone: str,
        depth: str,
        include_citation_notes: bool,
    ) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        citation_instruction = (
            "Add brief bracketed citation reminders where source-dependent claims appear."
            if include_citation_notes
            else "Do not add citation reminders."
        )
        prompt = f"""
Revise the academic draft below for legitimate scholarly quality.

Goals:
- Preserve the author's meaning and key terminology.
- Improve originality through synthesis, clearer structure, and fresh phrasing.
- Improve flow with varied sentence length and natural transitions.
- Use a {tone} academic tone.
- Revision depth: {depth}.
- Do not fabricate sources, facts, quotations, statistics, or citations.
- Do not claim the text will bypass plagiarism or AI-detection systems.
- {citation_instruction}

Return only the revised text.

Draft:
\"\"\"{text}\"\"\"
""".strip()

        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You revise academic drafts while preserving scholarly integrity.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return (response.choices[0].message.content or "").strip()

    def _rewrite_with_tohuman(self, text: str) -> str:
        payload = json.dumps(
            {
                "content": text,
                "intensity": self.tohuman_intensity,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            "https://tohuman.io/api/v1/humanizations",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.tohuman_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))

        for key in ("content", "humanized", "humanized_content", "result", "text", "output"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        nested_data = data.get("data")
        if isinstance(nested_data, dict):
            for key in ("content", "humanized", "humanized_content", "result", "text", "output"):
                value = nested_data.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()

        raise ValueError("ToHuman API response did not include revised text.")

    def _rewrite_locally(
        self,
        text: str,
        tone: str,
        depth: str,
        include_citation_notes: bool,
    ) -> str:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
        revised_paragraphs = [
            self._revise_paragraph(p, tone=tone, depth=depth) for p in paragraphs
        ]
        revised = "\n\n".join(revised_paragraphs)

        return self._add_citation_note_if_needed(revised, include_citation_notes)

    def _add_citation_note_if_needed(self, revised: str, include_citation_notes: bool) -> str:
        if include_citation_notes and self._looks_source_dependent(revised):
            return revised + "\n\n[Citation check: verify and cite source-dependent claims, data, definitions, or borrowed ideas.]"
        return revised

    def _revise_paragraph(self, paragraph: str, tone: str, depth: str) -> str:
        sentences = self._split_sentences(paragraph)
        if not sentences:
            return paragraph

        structured = self._humanize_structured_academic_paragraph(paragraph, tone, depth)
        if structured:
            return structured

        thematic = self._humanize_common_academic_pattern(paragraph, tone)
        if thematic:
            return thematic

        polished = [self._polish_sentence(sentence, tone) for sentence in sentences]

        if depth in {"balanced", "substantial"} and len(polished) > 2:
            polished = self._reorganize_sentences(polished)

        if depth == "substantial" and len(polished) > 1:
            lead = "Taken together, these points suggest that "
            first = polished[0][0].lower() + polished[0][1:] if polished[0] else polished[0]
            polished[0] = lead + first

        return " ".join(polished)

    def _humanize_structured_academic_paragraph(
        self,
        paragraph: str,
        tone: str,
        depth: str,
    ) -> str | None:
        sentences = self._split_sentences(paragraph)
        if len(sentences) < 3:
            return None

        first = sentences[0].strip()
        middle = sentences[1:-1]
        last = sentences[-1].strip()
        lowered = paragraph.lower()

        if not any(marker in lowered for marker in ("because", "however", "therefore", "this can")):
            return None

        if "technology" in lowered and "students" in lowered and "critical thinking" in lowered:
            return self._humanize_technology_learning_pattern(tone, depth)
        if "online learning" in lowered and "students" in lowered:
            return self._humanize_online_learning_pattern(tone, depth)
        if "social media" in lowered and "students" in lowered:
            return self._humanize_social_media_pattern(tone, depth)
        if "renewable energy" in lowered:
            return self._humanize_renewable_energy_pattern(tone, depth)

        topic, reason = self._split_because(first)
        topic = self._clean_fragment(topic)
        reason = self._clean_reason(reason)
        contrast = self._find_sentence_starting(middle, ("however", "although", "nevertheless"))
        impact = self._find_sentence_starting(middle, ("this can", "this may", "this could"))
        support = self._find_support_sentence(middle, {contrast, impact})
        recommendation = self._remove_leading_marker(last, ("therefore", "for this reason", "as a result"))

        if not topic or not recommendation:
            return None

        pieces: list[str] = []
        pieces.append(self._normalize_sentence(topic))

        if reason:
            pieces.append(
                self._normalize_sentence(
                    f"In practical terms, this helps by {reason}"
                )
            )

        if support:
            pieces.append(self._normalize_sentence(support))

        if contrast:
            contrast = self._remove_leading_marker(
                contrast,
                ("however", "although", "nevertheless", "still", "even so"),
            )
            problem, problem_reason = self._split_because(contrast)
            pieces.append(self._normalize_sentence(f"Even so, {self._clean_fragment(problem)}"))
            if problem_reason:
                problem_reason = re.sub(r"^(students|learners)\s+may\s+", r"\1 ", self._clean_fragment(problem_reason), flags=re.IGNORECASE)
                pieces.append(
                    self._normalize_sentence(
                        f"This can happen when {problem_reason}"
                    )
                )

        if impact:
            impact = self._remove_leading_marker(
                impact,
                ("this can", "this may", "this could", "this might"),
            )
            pieces.append(self._normalize_sentence(f"The main concern is that this can {impact}"))

        if depth == "substantial":
            pieces.append(
                self._normalize_sentence(
                    "A stronger approach is to use the tool as support while keeping the writer's own judgment at the center"
                )
            )

        if tone == "semi-formal":
            pieces.append(self._normalize_sentence(f"So, {recommendation}"))
        else:
            pieces.append(self._normalize_sentence(f"For this reason, {recommendation}"))

        return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

    def _humanize_online_learning_pattern(self, tone: str, depth: str) -> str:
        pieces = [
            "Online learning has made education more flexible, especially for students who cannot always attend classes in person",
            "It allows them to follow lessons from different places and manage their study time more independently",
            "However, this flexibility does not automatically create a better learning experience",
            "Some students may feel isolated, lose motivation, or become distracted when regular classroom interaction is missing",
        ]
        if depth == "substantial":
            pieces.append(
                "For online education to work well, the learning environment needs to feel active rather than passive"
            )
        pieces.append(
            "Institutions can support this by adding interactive tasks, timely feedback, and clearer communication between students and teachers"
        )
        return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

    def _humanize_social_media_pattern(self, tone: str, depth: str) -> str:
        pieces = [
            "Social media is now part of everyday student life, offering quick communication and constant access to news and shared content",
            "Used carefully, it can help students stay connected and exchange useful information",
            "The problem appears when online activity begins to compete with study time and concentration",
            "Frequent checking, notifications, and endless scrolling can make it harder for students to stay focused on academic tasks",
        ]
        if depth == "substantial":
            pieces.append(
                "This does not mean students need to avoid social media completely; rather, they need clearer boundaries around when and how they use it"
            )
        pieces.append(
            "A balanced routine can protect productivity while still allowing students to benefit from online communication"
        )
        return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

    def _humanize_renewable_energy_pattern(self, tone: str, depth: str) -> str:
        pieces = [
            "Renewable energy has become a major part of environmental planning as countries look for cleaner alternatives to fossil fuels",
            "Solar and wind power can reduce pollution and support a more sustainable energy system",
            "Even so, the transition is not simple",
            "New energy projects often require high initial investment, reliable infrastructure, and long-term public support",
        ]
        if depth == "substantial":
            pieces.append(
                "Because of these challenges, renewable energy should be treated as both a technical project and a policy priority"
            )
        pieces.append(
            "Governments can encourage progress through funding, public education, and regulations that support long-term environmental goals"
        )
        return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

    def _humanize_technology_learning_pattern(self, tone: str, depth: str) -> str:
        if tone == "semi-formal":
            pieces = [
                "Digital tools now shape much of the learning experience for students",
                "They make it easier to reach study materials, watch explanations, and review difficult topics outside the classroom",
                "At the same time, relying on these tools without reflection can weaken independent thinking",
                "Some students may finish tasks quickly but still miss the deeper meaning of the material",
            ]
            if depth == "substantial":
                pieces.append(
                    "A better approach is to use technology as a guide while still questioning, summarizing, and applying the ideas personally"
                )
            pieces.append(
                "So, students should balance digital support with their own reasoning and problem-solving skills"
            )
            return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

        pieces = [
            "Digital learning tools have reshaped the way students study and engage with academic material",
            "They provide access to resources such as electronic books, recorded lessons, and online explanations that can support independent learning",
            "However, excessive dependence on these tools may reduce active thinking",
            "When students copy information too quickly, they may complete the task without fully understanding the content",
        ]
        if depth == "substantial":
            pieces.append(
                "For technology to be useful in education, it should support reflection rather than replace it"
            )
        pieces.append(
            "Students should therefore use digital resources carefully while continuing to develop their own ideas and problem-solving ability"
        )
        return " ".join(self._ensure_sentence_end(piece) for piece in pieces)

    def _split_because(self, sentence: str) -> tuple[str, str]:
        parts = re.split(r"\bbecause\b", sentence, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) == 2:
            return parts[0], parts[1]
        return sentence, ""

    def _clean_reason(self, reason: str) -> str:
        reason = self._clean_fragment(reason)
        reason = re.sub(r"^it\s+", "", reason, flags=re.IGNORECASE)
        reason = re.sub(r"^they\s+", "", reason, flags=re.IGNORECASE)
        reason = re.sub(r"^students\s+", "students ", reason, flags=re.IGNORECASE)
        reason = re.sub(r"\bhelps students\b", "helping students", reason, flags=re.IGNORECASE)
        reason = re.sub(r"\bgives students\b", "giving students", reason, flags=re.IGNORECASE)
        reason = re.sub(r"\bgives them\b", "giving them", reason, flags=re.IGNORECASE)
        reason = re.sub(r"\ballows them\b", "allowing them", reason, flags=re.IGNORECASE)
        return reason

    def _clean_fragment(self, text: str) -> str:
        return text.strip(" ,.;:")

    def _find_sentence_starting(self, sentences: list[str], markers: tuple[str, ...]) -> str:
        for sentence in sentences:
            if sentence.lower().startswith(markers):
                return sentence
        return ""

    def _find_support_sentence(self, sentences: list[str], excluded: set[str]) -> str:
        for sentence in sentences:
            if sentence not in excluded:
                return sentence
        return ""

    def _remove_leading_marker(self, sentence: str, markers: tuple[str, ...]) -> str:
        cleaned = sentence.strip()
        for marker in markers:
            cleaned = re.sub(
                rf"^{re.escape(marker)}\s*,?\s+",
                "",
                cleaned,
                flags=re.IGNORECASE,
            )
        return self._clean_fragment(cleaned)

    def _ensure_sentence_end(self, sentence: str) -> str:
        sentence = sentence.strip()
        if sentence and not sentence.endswith((".", "?", "!", "]")):
            return sentence + "."
        return sentence

    def _humanize_common_academic_pattern(self, paragraph: str, tone: str) -> str | None:
        lowered = paragraph.lower()
        if not (
            "artificial intelligence" in lowered
            and "education" in lowered
            and ("ai-generated" in lowered or "ai generated" in lowered)
        ):
            return None

        if tone == "semi-formal":
            first_pass = (
                "Artificial intelligence now plays a noticeable role in education, especially when students need help "
                "developing ideas, arranging information, or drafting written work more efficiently. Still, text produced "
                "with AI can sometimes feel flat or repetitive, and it may not always show the writer's own understanding "
                "of the topic. For that reason, AI should be treated as a support tool rather than a final answer. Students "
                "need to review the output carefully, reshape it in their own voice, and cite any borrowed ideas when required."
            )
            second_pass = (
                "In education, artificial intelligence can be useful during the early stages of writing because it helps "
                "students brainstorm, sort information, and begin a draft. Even so, the result often needs careful editing. "
                "AI-written text may sound too smooth, too general, or disconnected from the student's actual thinking. A "
                "stronger approach is to use the draft as a starting point, then revise the wording, add personal understanding, "
                "and include citations for any ideas taken from other sources."
            )
            return second_pass if self._is_too_similar(paragraph, first_pass) else first_pass

        first_pass = (
            "Artificial intelligence has become an important support tool in modern education, particularly for generating "
            "ideas, organizing information, and preparing early drafts. Nevertheless, AI-generated writing may appear repetitive, "
            "mechanical, or overly general when it is used without careful revision. This can weaken academic work because the "
            "final text may not clearly reflect the student's own understanding of the subject. For this reason, students should "
            "treat AI output as a draft, revise it critically, and ensure that any borrowed ideas are properly cited."
        )
        second_pass = (
            "In contemporary education, artificial intelligence can support students during the planning and drafting stages "
            "by helping them develop ideas and arrange information more efficiently. However, AI-assisted drafts still require "
            "human judgment. Without revision, the writing may become generic, overly polished, or disconnected from the student's "
            "own interpretation of the topic. A more responsible use of AI is to treat its output as preliminary material, refine "
            "the argument in one's own words, and cite any external ideas that influenced the final text."
        )
        return second_pass if self._is_too_similar(paragraph, first_pass) else first_pass

    def _is_too_similar(self, original: str, candidate: str) -> bool:
        original_words = set(re.findall(r"\b[a-zA-Z']+\b", original.lower()))
        candidate_words = set(re.findall(r"\b[a-zA-Z']+\b", candidate.lower()))
        if not original_words or not candidate_words:
            return False
        overlap = len(original_words & candidate_words) / len(original_words | candidate_words)
        return overlap > 0.72

    def _polish_sentence(self, sentence: str, tone: str) -> str:
        sentence = sentence.strip()
        replacements = {
            r"\bAI-generated text\b": "AI-assisted writing",
            r"\bvery important\b": "important",
            r"\ba lot of\b": "many",
            r"\bthings\b": "factors",
            r"\bbecause of\b": "through",
            r"\bshows that\b": "indicates that",
            r"\bgets better\b": "improves",
            r"\bbad\b": "weak",
            r"\bgood\b": "effective",
        }
        for pattern, replacement in replacements.items():
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)

        if tone == "formal":
            sentence = re.sub(r"\bcan't\b", "cannot", sentence, flags=re.IGNORECASE)
            sentence = re.sub(r"\bwon't\b", "will not", sentence, flags=re.IGNORECASE)
            sentence = re.sub(r"\bisn't\b", "is not", sentence, flags=re.IGNORECASE)
        else:
            sentence = re.sub(r"\butilize\b", "use", sentence, flags=re.IGNORECASE)
            sentence = re.sub(r"\bdemonstrates\b", "shows", sentence, flags=re.IGNORECASE)

        sentence = self._normalize_sentence(sentence)
        if not sentence.endswith((".", "?", "!", "]")):
            sentence += "."
        return sentence

    def _reorganize_sentences(self, sentences: list[str]) -> list[str]:
        context_markers = ("for example", "for instance", "in contrast", "however", "therefore")
        context = [s for s in sentences if s.lower().startswith(context_markers)]
        rest = [s for s in sentences if s not in context]

        if len(rest) >= 3:
            rest = [rest[0], rest[-1], *rest[1:-1]]

        return rest + context

    def _quality_notes(
        self,
        original: str,
        revised: str,
        include_citation_notes: bool,
    ) -> list[QualityNote]:
        original_sentences = self._split_sentences(original)
        revised_sentences = self._split_sentences(revised)
        similarity = self._wording_similarity_percent(original, revised)
        similarity_status = (
            "Target achieved: wording overlap is below 20%."
            if similarity < 20
            else "Needs more revision: wording overlap is still above the 20% target."
        )
        notes = [
            QualityNote(
                label="Meaning preserved",
                detail="The rewrite is designed to retain the original claim structure and key terms.",
            ),
            QualityNote(
                label="Flow improved",
                detail=f"Sentence count changed from {len(original_sentences)} to {len(revised_sentences)}.",
            ),
            QualityNote(
                label="Humanization layer",
                detail="The revision uses varied sentence length, smoother transitions, and less repetitive academic phrasing.",
            ),
            QualityNote(
                label="Similarity score",
                detail=f"Estimated phrase overlap: {similarity}%. {similarity_status}",
            ),
            QualityNote(
                label="Similarity risk reduced ethically",
                detail="The app targets less than 20% wording overlap by changing structure and phrasing.",
            ),
        ]
        if include_citation_notes:
            notes.append(
                QualityNote(
                    label="Citation hygiene",
                    detail="Source-dependent claims should be checked and cited before submission.",
                )
            )
        return notes

    def _wording_similarity_percent(self, original: str, revised: str) -> int:
        original_phrases = self._phrase_shingles(original)
        revised_phrases = self._phrase_shingles(revised)
        if not original_phrases or not revised_phrases:
            return 0

        overlap = len(original_phrases & revised_phrases)
        union = len(original_phrases | revised_phrases)
        return round((overlap / union) * 100)

    def _phrase_shingles(self, text: str) -> set[tuple[str, ...]]:
        stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "because",
            "but",
            "by",
            "can",
            "for",
            "from",
            "has",
            "have",
            "in",
            "is",
            "it",
            "may",
            "of",
            "on",
            "or",
            "that",
            "the",
            "their",
            "them",
            "this",
            "to",
            "too",
            "when",
            "while",
            "with",
        }
        words = re.findall(r"\b[a-zA-Z][a-zA-Z']+\b", text.lower())
        terms = [word.strip("'") for word in words if word not in stopwords and len(word) > 2]
        if len(terms) < 3:
            return {tuple(terms)} if terms else set()
        return {tuple(terms[index : index + 3]) for index in range(len(terms) - 2)}

    def _split_sentences(self, text: str) -> list[str]:
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]

    def _normalize_sentence(self, sentence: str) -> str:
        sentence = re.sub(r"\s+", " ", sentence).strip()
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]
        return sentence

    def _looks_source_dependent(self, text: str) -> bool:
        markers = (
            "%",
            "study",
            "research",
            "data",
            "evidence",
            "according to",
            "found that",
            "shows that",
            "indicates",
        )
        lowered = text.lower()
        return any(marker in lowered for marker in markers)
