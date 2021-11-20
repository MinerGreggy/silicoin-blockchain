


from decimal import Decimal
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint8, uint64, uint128


def calculate_iterations_quality(
    difficulty_constant_factor: uint128,
    quality_string: bytes32,
    size: int,
    difficulty: uint64,
    difficulty_coeff: Decimal,
    cc_sp_output_hash: bytes32,
) -> uint64:
    """
    Calculates the number of iterations from the quality. This is derives as the difficulty times the constant factor
    times a random number between 0 and 1 (based on quality string), divided by plot size.
    """
    sp_quality_string: bytes32 = std_hash(quality_string + cc_sp_output_hash)

    log.error(f"Rook its {difficulty_constant_factor} {quality_string} {size} {difficulty} {difficulty_coeff} {cc_sp_output_hash}")
    iters = uint64(
        int(difficulty * difficulty_coeff)
        * int(difficulty_constant_factor)
        * int.from_bytes(sp_quality_string, "big", signed=False)
        // (int(pow(2, 256)) * int(_expected_plot_size(size)))
    )
    return max(iters, uint64(1))


def calculate_required_difficulty(total_iters: uint64, header_iters: uint64, difficulty_coeff: Decimal) -> Decimal:
    reduced_iters = uint64(total_iters / int(difficulty_coeff*4704))
    needed_diff = Decimal(header_iters / (reduced_iters * 4704))
    print(f"diff_coef {difficulty_coeff} needed_diff {needed_diff}")
    print(f"difference {difficulty_coeff - needed_diff}")
    return needed_diff


if __name__=="__main__":
    calculate_required_difficulty(uint64(102991600193), uint64(102991600299), Decimal(0.9821240585624592261063228199))
