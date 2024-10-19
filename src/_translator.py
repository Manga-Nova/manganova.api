from typing import Any, ClassVar, Self

from fluent.runtime import FluentLocalization, FluentResourceLoader

from src._types import LanguageEnum


class Translator:
    """
    Singleton class for managing translations of ApiError classes.
    """

    _instance: Self | None = None

    _resources = FluentResourceLoader(
        roots="src/locales/{locale}",
    )

    _mappings: ClassVar[dict[LanguageEnum, FluentLocalization]] = {
        LanguageEnum.ENGLISH: FluentLocalization(
            locales=["en"],
            resource_ids=["translations.ftl"],
            resource_loader=_resources,
        ),
        LanguageEnum.PORTUGUESE: FluentLocalization(
            locales=["pt"],
            resource_ids=["translations.ftl"],
            resource_loader=_resources,
        ),
    }

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_locale(self, language: LanguageEnum | str) -> FluentLocalization:
        if isinstance(language, str):
            language = LanguageEnum(language)
        return self._mappings[language]

    async def translate(
        self,
        *,
        key: str,
        language: LanguageEnum | str,
        **kwargs: Any,  # noqa: ANN401
    ) -> str:
        """
        Translate a key to a given language.
        """
        l10n = self._get_locale(language)
        return l10n.format_value(key, **kwargs)
