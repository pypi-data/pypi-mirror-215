from playwright.sync_api import Playwright
import pytest
from qashared.helpers import *
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace

@pytest.fixture
def global_context():
    return DividoSimpleNamespace()

@pytest.fixture
def test_context():
    return DividoSimpleNamespace()

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture
def page(playwright: Playwright, config: DividoSimpleNamespace, test_context: DividoSimpleNamespace):
    browser = playwright.chromium.launch(headless=config.playwright.headless)
    context = browser.new_context(
        viewport=config.playwright.viewport.__dict__,
        record_video_dir=f'test_results/{test_context.feature_name}/{test_context.scenario_name}/videos', 
        record_video_size = (config.playwright.viewport.__dict__))
    
    yield context.new_page()

    context.close()
    
@pytest.fixture(scope="session")
def test_data(config):
    return add_test_data_from_files(DividoSimpleNamespace(), directory=f'./data/{config.verify_attributes("environment").environment}')
