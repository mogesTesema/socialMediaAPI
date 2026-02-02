"""
Load the ONNX food vision model and provide a prediction helper.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Sequence, Tuple, Union

import numpy as np
import onnxruntime as ort
from PIL import Image
from storeapi.food_vision_model.preprocessing import prepare_batch, prepare_image

MODEL_PATH = Path(__file__).with_name("food_vision_model.onnx")


@lru_cache(maxsize=1)
def load_food_vision_model(
	model_path: Union[str, Path] = MODEL_PATH,
) -> ort.InferenceSession:
	"""Load the ONNX model and return a ready-to-run inference session."""
	model_path = Path(model_path)
	if not model_path.exists():
		raise FileNotFoundError(f"Model file not found: {model_path}")
	return ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])


def _softmax(logits: np.ndarray) -> np.ndarray:
	logits = logits - np.max(logits)
	exp = np.exp(logits)
	return exp / np.sum(exp)


def _onnx_input_dtype(input_type: str) -> np.dtype:
	if "float" in input_type:
		return np.float32
	if "uint8" in input_type:
		return np.uint8
	if "int8" in input_type:
		return np.int8
	return np.float32




def predict_food(
	image: Union[str, Path, bytes, Image.Image],
	labels: Sequence[str] | None = None,
	top_k: int | None = None,
) -> List[Tuple[str, float]]:
	"""
	Predict food item(s) from an image.

	Returns a list of (label, score) tuples ordered by score.
	If labels is None, the label will be the class index as a string.
	"""
	if top_k is not None and top_k < 1:
		raise ValueError("top_k must be >= 1")

	session = load_food_vision_model()
	input_info = session.get_inputs()[0]
	output_info = session.get_outputs()[0]

	input_shape = input_info.shape
	input_dtype = _onnx_input_dtype(input_info.type)
	input_tensor = prepare_image(image, input_shape, input_dtype)

	output = session.run([output_info.name], {input_info.name: input_tensor})[0].squeeze()
	if output.ndim == 0:
		output = np.array([float(output)])

	if np.issubdtype(output.dtype, np.floating):
		if not np.isclose(np.sum(output), 1.0, atol=1e-3):
			output = _softmax(output.astype(np.float32))

	if top_k is None:
		indices = np.argsort(output)[::-1]
	else:
		top_k = min(top_k, output.shape[0])
		indices = np.argsort(output)[-top_k:][::-1]

	results: List[Tuple[str, float]] = []
	for idx in indices:
		idx_int = int(idx)
		label = (
			labels[idx_int]
			if labels and idx_int < len(labels)
			else str(idx_int)
		)
		results.append((label, float(output[idx_int])))

	return results


def predict_food_batch(
	images: Sequence[Union[str, Path, bytes, Image.Image]],
	labels: Sequence[str] | None = None,
	top_k: int | None = 1,
) -> List[List[Tuple[str, float]]]:
	if top_k is not None and top_k < 1:
		raise ValueError("top_k must be >= 1")

	session = load_food_vision_model()
	input_info = session.get_inputs()[0]
	output_info = session.get_outputs()[0]

	input_shape = input_info.shape
	input_dtype = _onnx_input_dtype(input_info.type)
	input_tensor = prepare_batch(images, input_shape, input_dtype)

	output = session.run([output_info.name], {input_info.name: input_tensor})[0]
	if output.ndim == 1:
		output = np.expand_dims(output, axis=0)

	results: List[List[Tuple[str, float]]] = []
	for row in output:
		row_scores = row
		if np.issubdtype(row_scores.dtype, np.floating):
			if not np.isclose(np.sum(row_scores), 1.0, atol=1e-3):
				row_scores = _softmax(row_scores.astype(np.float32))

		if top_k is None:
			indices = np.argsort(row_scores)[::-1]
		else:
			k = min(top_k, row_scores.shape[0])
			indices = np.argsort(row_scores)[-k:][::-1]

		row_results: List[Tuple[str, float]] = []
		for idx in indices:
			idx_int = int(idx)
			label = (
				labels[idx_int]
				if labels and idx_int < len(labels)
				else str(idx_int)
			)
			row_results.append((label, float(row_scores[idx_int])))
		results.append(row_results)

	return results


def demo_steak_prediction(
	top_k: int = 3,
	labels: Sequence[str] | None = None,
	image_shape: Tuple[int, int, int] = (244, 244, 3),
) -> List[Tuple[str, float]]:
	"""
	Create a synthetic steak-like image (244x244x3) and print predictions.
	"""
	height, width, channels = image_shape
	if channels != 3:
		raise ValueError("image_shape must have 3 channels")

	# Create a steak-like RGB texture: reddish center with darker edges.
	base = np.zeros((height, width, 3), dtype=np.uint8)
	base[..., 0] = 140  # red
	base[..., 1] = 60   # green
	base[..., 2] = 50   # blue

	yy, xx = np.ogrid[:height, :width]
	center_y, center_x = height / 2, width / 2
	radius = min(height, width) * 0.35
	mask = (yy - center_y) ** 2 + (xx - center_x) ** 2 <= radius ** 2
	base[mask] = [180, 80, 65]

	image = Image.fromarray(base, mode="RGB")
	results = predict_food(image, labels=labels, top_k=top_k)

	print("Demo steak prediction results:")
	for label, score in results:
		print(f"- {label}: {score:.4f}")

	return results
