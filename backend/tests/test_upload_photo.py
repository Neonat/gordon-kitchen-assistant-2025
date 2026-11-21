import base64
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


class UploadPhotoTests(unittest.TestCase):
    def setUp(self):
        image_module = types.ModuleType("utils.imagerec")
        image_module.img_detect_items = Mock(return_value="rice,yoghurt")
        api_tool = types.ModuleType("utils.api_tool")
        api_tool.get_recipe_instruction = Mock()
        ai = types.ModuleType("ai")
        ai.graph = Mock()
        ai.process_user_input = Mock(return_value="Recipe response")
        spoonacular = types.ModuleType("spoonacular")
        spoonacular.SearchRecipes200ResponseResultsInner = Mock()
        spec = importlib.util.spec_from_file_location("camera_app", Path(__file__).parents[1] / "app.py")
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {
            "utils.imagerec": image_module, "utils.api_tool": api_tool,
            "ai": ai, "spoonacular": spoonacular,
        }):
            spec.loader.exec_module(self.module)
        self.client = self.module.app.test_client()
        self.detector = image_module.img_detect_items
        self.photo = "data:image/png;base64," + base64.b64encode(b"captured image bytes").decode()

    def test_photo_reaches_detector_and_returns_items(self):
        paths = []

        def detect(path, mime_type="image/jpeg"):
            self.assertEqual(Path(path).read_bytes(), b"captured image bytes")
            self.assertEqual(mime_type, "image/png")
            paths.append(Path(path))
            return "rice,yoghurt"

        self.detector.side_effect = detect
        response = self.client.post("/api/upload-photo", json={"photo": self.photo})
        self.assertEqual(response.status_code, 200, response.get_json())
        self.assertEqual(response.get_json(), {"detected_items": "rice,yoghurt"})
        self.assertEqual(len(paths), 1)
        self.assertFalse(paths[0].exists())

    def test_missing_photo_does_not_call_detector(self):
        self.assertEqual(self.client.post("/api/upload-photo", json={}).status_code, 400)
        self.detector.assert_not_called()

    def test_detector_failure_cleans_up_image(self):
        paths = []

        def fail(path, **kwargs):
            paths.append(Path(path))
            raise RuntimeError("Image service unavailable")

        self.detector.side_effect = fail
        response = self.client.post("/api/upload-photo", json={"photo": self.photo})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(len(paths), 1)
        self.assertFalse(paths[0].exists())


if __name__ == "__main__":
    unittest.main()
