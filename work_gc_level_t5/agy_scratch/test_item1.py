from fractions import Fraction

def bfs_drifts():
    # Level E:
    # S^E_0 = {-1, 0, 1}, S^E_1 = {-1, 0, 1}, S^E_2 = set()
    S_E = [{-1, 0, 1}, {-1, 0, 1}, set()]
    cur_E = {Fraction(1)}
    levels_E = [cur_E]
    for t in range(3):
        nxt = set()
        for th in cur_E:
            nxt.add(3 - th)
            nxt.add(th - 1)
            for s in S_E[t]:
                nxt.add(th + s)
        levels_E.append(nxt)
        cur_E = nxt

    # S(J) (Level T5):
    # S_0 = [-2, 2] U {4/3}
    # S_1 = {-1, 0, 1}
    # S_2 = {-1, 0, 1}
    # S_3 = set()
    # S_4 = set()
    S_T5 = [
        {-2, -1, 0, 1, 2, Fraction(4, 3)},
        {-1, 0, 1},
        {-1, 0, 1},
        set(),
        set()
    ]
    cur_T5 = {Fraction(1)}
    levels_T5 = [cur_T5]
    for t in range(4):
        nxt = set()
        for th in cur_T5:
            nxt.add(3 - th)
            nxt.add(th - 1)
            for s in S_T5[t]:
                nxt.add(th + s)
        levels_T5.append(nxt)
        cur_T5 = nxt

    print("=== Level E Drifts ===")
    for t, s in enumerate(levels_E):
        ints = sorted([int(x) for x in s if x.denominator == 1])
        rats = sorted([x for x in s if x.denominator != 1])
        print(f"t={t}: ints={ints}, rats={rats}")

    print("\n=== S(J) Drifts ===")
    for t, s in enumerate(levels_T5):
        ints = sorted([int(x) for x in s if x.denominator == 1])
        rats = sorted([f"{x.numerator}/{x.denominator}" for x in s if x.denominator != 1])
        print(f"t={t}: ints={ints}, rats={rats}")

    # Check NOTES §2 table
    # t=0: Theta^E_0={1}, ints={1}, rats=empty
    # t=1: Theta^E_1={0,1,2}, ints=[-1,3], rats={7/3}
    # t=2: Theta^E_2=[-1,3], ints=[-2,4], rats={2/3, 4/3, 7/3, 10/3}
    # t=3: Theta^E_3=[-2,4], ints=[-3,5], rats={-1/3, 1/3, 2/3, 4/3, 5/3, 7/3, 10/3, 13/3}
    # t=4: ints=[-4,6], rats={-4/3, -2/3, -1/3, 1/3, 2/3, 4/3, 5/3, 7/3, 8/3, 10/3}

    notes_E_ints = [
        [1],
        [0, 1, 2],
        [-1, 0, 1, 2, 3],
        [-2, -1, 0, 1, 2, 3, 4]
    ]
    notes_T5_ints = [
        [1],
        [-1, 0, 1, 2, 3],
        [-2, -1, 0, 1, 2, 3, 4],
        [-3, -2, -1, 0, 1, 2, 3, 4, 5],
        [-4, -3, -2, -1, 0, 1, 2, 3, 4, 6] # wait, note says [-4, 6], let's check
    ]
    notes_T5_rats = [
        [],
        ['7/3'],
        ['2/3', '4/3', '7/3', '10/3'],
        ['-1/3', '1/3', '2/3', '4/3', '5/3', '7/3', '10/3', '13/3'],
        ['-4/3', '-2/3', '-1/3', '1/3', '2/3', '4/3', '5/3', '7/3', '8/3', '10/3']
    ]

    for t in range(4):
        actual_E_ints = sorted([int(x) for x in levels_E[t]])
        assert actual_E_ints == notes_E_ints[t], f"E ints mismatch at t={t}: {actual_E_ints} vs {notes_E_ints[t]}"
        assert all(x.denominator == 1 for x in levels_E[t]), f"E has rational at t={t}"

    for t in range(5):
        actual_T5_ints = sorted([int(x) for x in levels_T5[t] if x.denominator == 1])
        actual_T5_rats = sorted([f"{x.numerator}/{x.denominator}" for x in levels_T5[t] if x.denominator != 1], key=lambda r: Fraction(r))
        expected_rats = sorted(notes_T5_rats[t], key=lambda r: Fraction(r))
        print(f"\nChecking t={t}:")
        print(f"  actual ints: {actual_T5_ints}")
        expected_range = list(range(notes_T5_ints[t][0], notes_T5_ints[t][-1] + 1))
        assert actual_T5_ints == expected_range, f"T5 ints mismatch at t={t}: {actual_T5_ints} vs {expected_range}"
        print(f"  actual rats: {actual_T5_rats}")
        print(f"  expect rats: {expected_rats}")
        assert actual_T5_rats == expected_rats, f"T5 rats mismatch at t={t}: {actual_T5_rats} vs {expected_rats}"

    # Specifically check Theta_4 contains -1/3 from 3 - 10/3:
    assert Fraction(10, 3) in levels_T5[3]
    assert Fraction(-1, 3) in levels_T5[4]
    assert (3 - Fraction(10, 3)) == Fraction(-1, 3)
    print("\nVerified: Theta_4 contains -1/3 = 3 - 10/3!")
    print("ALL ITEM 1 ASSERTIONS PASSED!")

if __name__ == "__main__":
    bfs_drifts()
