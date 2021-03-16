from typing import cast

import pytest
from faker import Faker

from overhave import db
from overhave.entities.converters import EmulationModel, FeatureTypeModel, SystemUserModel, TestUserModel
from overhave.entities.settings import OverhaveEmulationSettings
from overhave.storage.emulation import EmulationStorage


@pytest.fixture(scope="class")
def test_emulation_settings() -> OverhaveEmulationSettings:
    return OverhaveEmulationSettings()


@pytest.fixture(scope="class")
def test_emulation_storage(test_emulation_settings: OverhaveEmulationSettings) -> EmulationStorage:
    return EmulationStorage(test_emulation_settings)


@pytest.fixture()
def feature_type(database: None, faker: Faker) -> db.FeatureType:
    with db.create_session() as session:
        feature_type = db.FeatureType(name=cast(str, faker.word()))
        session.add(feature_type)
        session.flush()
        return cast(FeatureTypeModel, FeatureTypeModel.from_orm(feature_type))


@pytest.fixture()
def test_system_user(faker: Faker) -> SystemUserModel:
    with db.create_session() as session:
        app_user = db.UserRole(login=faker.word(), password=faker.word(), role=db.Role.user)
        session.add(app_user)
        session.flush()
        return cast(SystemUserModel, SystemUserModel.from_orm(app_user))


@pytest.fixture()
def test_user(test_system_user, faker: Faker, feature_type: FeatureTypeModel) -> TestUserModel:
    with db.create_session() as session:
        test_user = db.TestUser(
            feature_type_id=feature_type.id, name=cast(str, faker.word()), created_by=test_system_user.login
        )
        session.add(test_user)
        session.flush()
        return cast(TestUserModel, TestUserModel.from_orm(test_user))


@pytest.fixture()
def test_emulation(test_system_user: SystemUserModel, test_user: TestUserModel, faker: Faker) -> EmulationModel:
    with db.create_session() as session:
        emulation = db.Emulation(
            name=cast(str, faker.word()),
            command=cast(str, faker.word()),
            test_user_id=test_user.id,
            created_by=test_system_user.login,
        )
        session.add(emulation)
        session.flush()
        return cast(EmulationModel, EmulationModel.from_orm(emulation))