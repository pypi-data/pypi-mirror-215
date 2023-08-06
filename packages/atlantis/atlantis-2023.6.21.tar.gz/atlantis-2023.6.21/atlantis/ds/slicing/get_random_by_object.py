import hashlib
import random


def get_random_by_object(obj, weights=None, seed=None):
	obj_str = str(obj)
	obj_type = type(obj).__name__
	obj_combined = f"{obj_type}.:.{obj_str}.:.{seed}"

	internal_seed = hashlib.sha256(obj_combined.encode()).hexdigest()
	if weights is None:
		random.seed(internal_seed)
		return random.random()
	else:
		random.seed(internal_seed)
		index = random.choices(range(len(weights)), weights=weights, k=1)[0]
		return index
