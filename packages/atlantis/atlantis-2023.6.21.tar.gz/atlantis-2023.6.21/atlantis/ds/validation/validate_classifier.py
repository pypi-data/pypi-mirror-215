import pandas as pd
import numpy as np
from multiprocessing import Pool


def validate_classifier(classifier, name, validation_pairs, echo, multiprocessing=False, n_jobs=None):
	def _get_evaluation(fold_num_minus_1, train_test_data):
		fold_num = fold_num_minus_1 + 1
		if echo:
			print(f'Fold: {fold_num}')
		evaluation = train_test_data.train_and_test(classifier=classifier)
		evaluation['fold'] = fold_num
		return evaluation

	if not multiprocessing:
		evaluations_list = []
		for fold_num_minus_1, train_test_data in enumerate(validation_pairs):
			evaluation = _get_evaluation(fold_num_minus_1=fold_num_minus_1, train_test_data=train_test_data)
			evaluations_list.append(evaluation)

	else:
		if n_jobs is None:
			if echo:
				print('Multiprocessing ...')

			with Pool() as pool:
				evaluations_list = pool.starmap(_get_evaluation, enumerate(validation_pairs))
		else:
			if not isinstance(n_jobs, int):
				raise TypeError(f'n_jobs of type {type(n_jobs)} is not supported')
			if n_jobs < 1:
				raise ValueError(f'n_jobs of {n_jobs} is less than 1')

			if echo:
				print(f'Multiprocessing with {n_jobs} concurrent jobs ...')

			with Pool(processes=n_jobs) as pool:
				evaluations_list = pool.starmap(_get_evaluation, enumerate(validation_pairs))

	all_data = pd.concat(evaluations_list)
	all_data['n_folds'] = 1
	columns = [
		'model_name', 'label', 'set', 'true_negative', 'true_positive', 'false_negative',
		'false_positive', 'n_folds'
	]
	agg = all_data[columns].groupby(['model_name', 'label', 'set'], as_index=False).sum()
	true_positive = agg['true_positive']
	false_positive = agg['false_positive']
	false_negative = agg['false_negative']
	true_negative = agg['true_negative']
	agg['precision'] = true_positive / (true_positive + false_positive)
	agg['recall'] = true_positive / (true_positive + false_negative)
	agg['f1_score'] = true_positive / (true_positive + 0.5 * (false_positive + false_negative))
	agg['accuracy'] = (true_positive + true_negative) / (
			true_positive + true_negative + false_positive + false_negative)
	agg['precision'] = np.where(true_positive == 0, 0, agg['precision'])
	agg['recall'] = np.where(true_positive == 0, 0, agg['recall'])
	agg['f1_score'] = np.where(true_positive == 0, 0, agg['f1_score'])

	if name is not None:
		agg['model_name'] = name
	return agg


def build_classifier_validator(validation_pairs, echo=1, multiprocessing=False, n_jobs=None):
	def classifier_validator(classifier, name):
		return validate_classifier(
			classifier=classifier, name=name, validation_pairs=validation_pairs, echo=echo,
			multiprocessing=multiprocessing, n_jobs=n_jobs
		)

	return classifier_validator
