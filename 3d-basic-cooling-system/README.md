# 3D Basic Cooling System

Browser lesson for Automotive Training Lab, built from the Unity CoolingLab scene.

## Students

Open [3D Basic Cooling System](https://olmandave.github.io/Automotive-Training-Lab/3d-basic-cooling-system/) in a current desktop browser with WebGL support. Unity does not need to be installed. Use the camera presets, simulation controls, cutaway toggle, temperature graph, and diagnostic faults in the lesson. The header links back to the lesson list and offers full-screen mode.

## Build and hosting

These are the exported browser files, not the editable Unity project. GitHub Pages serves them as static assets; `.nojekyll` avoids Jekyll processing. Compression is disabled in the Unity build, so custom Content-Encoding headers are unnecessary.

The exact exported WebAssembly runtime is stored as `Build/3d-basic-cooling-system.wasm.part1` and `.part2` to fit connector upload limits. `index.html` fetches them in order, joins them into an application/wasm Blob, and passes its URL to Unity. The reconstructed runtime matches the original exported file byte for byte.

For local testing, serve the repository through HTTP rather than opening index.html directly. To replace the build, export the Unity Web build again, replace all generated Build assets together, and update the runtime parts and wrapper if retaining this layout.
