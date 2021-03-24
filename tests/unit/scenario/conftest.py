from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from faker import Faker

from overhave.entities import (
    FeatureModel,
    FeatureTypeModel,
    OverhaveLanguageSettings,
    OverhaveScenarioCompilerSettings,
    ScenarioModel,
    TestExecutorContext,
    TestRunModel,
)
from overhave.entities.converters import TagsTypeModel
from overhave.scenario import ScenarioCompiler, ScenarioParser
from overhave.utils import get_current_time
from tests.objects import TestLanguageName, get_feature_extractor, get_test_feature_containers


@pytest.fixture()
def test_scenario_text(request: FixtureRequest, language_settings: OverhaveLanguageSettings) -> str:
    if hasattr(request, "param"):
        return str(request.param)  # type: ignore
    features = get_test_feature_containers()
    if language_settings.step_prefixes is None:
        lang = TestLanguageName.ENG
    else:
        lang = TestLanguageName.RUS
    return next(
        iter(
            feature.scenario for feature in features if feature.language is lang and feature.name.startswith("scenario")
        )
    )


@pytest.fixture()
def test_feature() -> FeatureModel:
    return FeatureModel(
        id=1,
        name="feature",
        author="keks",
        type_id=1,
        task=["OVERHAVE-1"],
        last_edited_by="overlord",
        released=False,
        feature_type=FeatureTypeModel(id=1, name=get_feature_extractor().feature_types[0]),
        feature_tags=[TagsTypeModel(id=1, value="tag1", created_by="qqq", created_at=get_current_time())],
    )


@pytest.fixture()
def test_testrun() -> TestRunModel:
    return TestRunModel(
        id=1,
        created_at=get_current_time(),
        scenario_id=1,
        name="test",
        start=get_current_time(),
        end=get_current_time(),
        executed_by="executor",
        status="SUCCESS",
        report_status="GENERATION_FAILED",
        report=None,
        traceback=None,
    )


@pytest.fixture()
def test_scenario(test_scenario_text: str, faker: Faker) -> ScenarioModel:
    return ScenarioModel(id=faker.random_int(), feature_id=faker.random_int(), text=test_scenario_text)


@pytest.fixture()
def test_processing_ctx(
    test_feature: FeatureModel, test_scenario: ScenarioModel, test_testrun: TestRunModel
) -> TestExecutorContext:
    return TestExecutorContext(feature=test_feature, scenario=test_scenario, test_run=test_testrun)


@pytest.fixture()
def test_scenario_compiler(
    language_settings: OverhaveLanguageSettings,
    test_compilation_settings: OverhaveScenarioCompilerSettings,
    task_links_keyword: Optional[str],
) -> ScenarioCompiler:
    return ScenarioCompiler(
        compilation_settings=test_compilation_settings,
        language_settings=language_settings,
        task_links_keyword=task_links_keyword,
    )


@pytest.fixture()
def test_scenario_parser(
    test_compilation_settings: OverhaveScenarioCompilerSettings,
    language_settings: OverhaveLanguageSettings,
    task_links_keyword: Optional[str],
) -> ScenarioParser:
    return ScenarioParser(
        compilation_settings=test_compilation_settings,
        language_settings=language_settings,
        feature_extractor=get_feature_extractor(),
        task_links_keyword=task_links_keyword,
    )
