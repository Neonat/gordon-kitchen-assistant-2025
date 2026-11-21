import React, { act } from "react";
import { createRoot } from "react-dom/client";
import PhotoPreview from "./PhotoPreview";

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

test("analyzes a captured photo with the camera API and displays its detected items", async () => {
  const container = document.createElement("div");
  const root = createRoot(container);
  const photo = "data:image/png;base64,aW1hZ2U=";
  const previousFetch = global.fetch;
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ detected_items: "rice,yoghurt" }),
  });
  const alert = jest.spyOn(window, "alert").mockImplementation(() => {});

  try {
    await act(async () => root.render(<PhotoPreview photo={photo} onClose={() => {}} />));
    await act(async () => container.querySelectorAll("button")[1].click());
    expect(global.fetch).toHaveBeenCalledWith("http://localhost:5000/api/upload-photo", expect.objectContaining({
      method: "POST",
      body: JSON.stringify({ photo }),
    }));
    expect(container.querySelector("pre").textContent).toBe("rice,yoghurt");
  } finally {
    await act(async () => root.unmount());
    global.fetch = previousFetch;
    alert.mockRestore();
  }
});
