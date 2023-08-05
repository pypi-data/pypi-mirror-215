from autora.experimentalist.sampler.novelty import novelty_sample, novelty_score_sample
import numpy as np

# Note: We encourage you to write more functionality tests for your sampler.

def test_output_dimensions():
    condition_pool = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    reference_conditions = np.array([[0, 0, 0, 0], [1, 1, 1, 1]])
    n = 2
    condition_pool_new = novelty_sample(condition_pool, reference_conditions, n)

    # Check that the sampler returns n experiment conditions
    assert condition_pool_new.shape == (n, condition_pool.shape[1])

def test_novelty_sample_1D():

    num_samples = 2

    # define two matrices
    matrix1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    matrix2 = np.array([1, 2, 3])

    # reorder matrix1 according to its distances to matrix2
    reordered_matrix1 = novelty_sample(condition_pool = matrix1,
                                        reference_conditions = matrix2,
                                        num_samples = num_samples)

    assert reordered_matrix1.shape[0] == num_samples
    assert reordered_matrix1.shape[1] == 1
    assert np.array_equal(reordered_matrix1, np.array([[10], [9]]))


def test_novelty_sample_ND():
    # define two matrices
    matrix1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    matrix2 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    num_samples = 2

    # reorder matrix1 according to its distances to matrix2
    reordered_matrix1 = novelty_sample(condition_pool = matrix1,
                                        reference_conditions = matrix2,
                                        num_samples = num_samples)

    assert reordered_matrix1.shape[0] == 2
    assert reordered_matrix1.shape[1] == 3
    assert np.array_equal(reordered_matrix1, np.array([[10, 11, 12], [7, 8, 9]]))

def test_novelty_score_sample_ND():
    # define two matrices
    matrix1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    matrix2 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    num_samples = 3

    # reorder matrix1 according to its distances to matrix2, and obtain distance score
    (reordered_matrix1, score) = novelty_score_sample(condition_pool=matrix1,
                                        reference_conditions=matrix2,
                                        num_samples=num_samples)

    assert score[0] > score[1]  and score[1] > score[2]