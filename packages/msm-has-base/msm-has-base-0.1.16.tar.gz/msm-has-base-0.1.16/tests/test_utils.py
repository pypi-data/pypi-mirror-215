from msm_has_base.utils import xor


def test_xor():
    # r = xor('4f6826fe75f12f58', '0100000000000000')
    r = xor('0B831502132C04FB', '1651101A239E252A')
    print(r)
    # print('abc'.encode('ascii').hex())
