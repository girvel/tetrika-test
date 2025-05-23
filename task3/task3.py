def appearance(intervals: dict[str, list[int]]) -> int:
    pupil = intervals["pupil"]
    tutor = intervals["tutor"]
    start, finish = intervals["lesson"]

    pupil_i = 0
    tutor_i = 0
    # indices instead of list copies for performance

    is_pupil_there = False
    is_tutor_there = False
    prev_t = None
    result = 0

    while pupil_i < len(pupil) or tutor_i < len(tutor):
        was_last_t_pupils = pupil_i < len(pupil) and (tutor_i >= len(tutor) or pupil[pupil_i] < tutor[tutor_i])
        if was_last_t_pupils:
            t = pupil[pupil_i]
            pupil_i += 1
        else:
            t = tutor[tutor_i]
            tutor_i += 1

        if prev_t is not None and is_pupil_there and is_tutor_there and t >= start:
            if t >= finish:
                result += finish - prev_t
                break

            assert prev_t <= t, "Timestamps are out of order, data rendered meaningless"
            result += t - prev_t

        if was_last_t_pupils:
            is_pupil_there ^= True
        else:
            is_tutor_there ^= True

        prev_t = t

    return result


tests = [
    {
        'intervals': {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        },
        'answer': 3117
    },
    # {
    #     'intervals': {
    #         'lesson': [1594702800, 1594706400],
    #         'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
    #                   1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
    #                   1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
    #                   1594706524, 1594706524, 1594706579, 1594706641],
    #         'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
    #     },
    #     'answer': 3577
    # },
    {
        'intervals': {
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
        },
        'answer': 3565
    },
]


if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
