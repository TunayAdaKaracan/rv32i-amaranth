import random
from fixedint import Int32, UInt32

from amaranth.sim import Simulator, SimulatorContext, Period

from processor.isa import AluOpFunct as AluOp # Hacky Hack
from processor.alu import ALU

TEST_RESULTS_DIR = "alu/"

def compute_result(task: AluOp, value1: int, value2: int):
    if task == AluOp.ADD:
        return int(UInt32(value1) + UInt32(value2))
    if task == AluOp.SUB:
        return int(UInt32(value1) - UInt32(value2))
    if task == AluOp.SLL:
        return int(UInt32(value1) << UInt32(value2 & 0b11111))
    if task == AluOp.SLT:
        return int(Int32(value1) < Int32(value2))
    if task == AluOp.SLTU:
        return int(UInt32(value1) < UInt32(value2))
    if task == AluOp.XOR:
        return int(UInt32(value1) ^ UInt32(value2))
    if task == AluOp.SRL:
        return int(UInt32(value1) >> UInt32(value2 & 0b11111))
    if task == AluOp.SRA:
        return int(Int32(value1) >> UInt32(value2 & 0b11111))
    if task == AluOp.OR:
        return int(UInt32(value1) | UInt32(value2))
    if task == AluOp.AND:
        return int(UInt32(value1) & UInt32(value2))

def create_test(task: AluOp, value1: int, value2: int):
    return [
                task.name,
                value1, 
                -value2 if task == AluOp.SUB else value2, 
                task & 0b111, 
                (task & 0b1000) << 2, 
                0b1,
                compute_result(task, value1, value2)
            ]

def print_test_details(test, actual_result):
    print(f"Operation Type: {test[0]}")
    print(f"Value1: {hex(test[1])}")
    print(f"Value2: {hex(test[2])}")
    print(f"funct3: {bin(test[3])}")
    print(f"funct7: {bin(test[4])}")
    print(f"Immedi: {bin(test[5])}")
    print(f"Expected Result: {hex(test[6])}")
    print(f"Actual Result: {hex(actual_result)}")

# Does about 20290 tests including random tests
def alu_tests(do_random: bool = True, return_at_first_error: bool = True):
    print("============= ALU =============")
    print("Generating Tests...")

    TESTS = []
    OPS = [
        AluOp.ADD,
        AluOp.SUB,
        AluOp.SLL,
        AluOp.SLT,
        AluOp.SLTU,
        AluOp.XOR,
        AluOp.SRL,
        AluOp.SRA,
        AluOp.OR,
        AluOp.AND
    ]

    # Deterministic Tests
    for op in OPS:
        TESTS.append(create_test(op, 0, 0))
        TESTS.append(create_test(op, 1, 0))
        TESTS.append(create_test(op, 0, 1))
        TESTS.append(create_test(op, 1, 1))
        TESTS.append(create_test(op, 0xffffffff, 0xffffffff))
        for x in range(32):
            for y in range(32):
                TESTS.append(create_test(op, x, y))

    # Random tests, n=1000
    if do_random:
        for op in OPS:
            for _ in range(1000):
                value1 = random.randint(0, 0xffffffff)
                value2 = random.randint(0, 0xffffffff)
                TESTS.append(create_test(op, value1, value2))

    total_tests = len(TESTS)
    print(f"Generated {total_tests} tests.")

    # Start simulation
    error = {
        "has_error": False,
        "actual_result": 0
    }

    def create_bench(test, err: dict):
        top = ALU()
        sim = Simulator(top)
        
        async def bench(ctx: SimulatorContext):
            ctx.set(top.value1, test[1])
            ctx.set(top.value2, test[2])
            ctx.set(top.funct3, test[3])
            ctx.set(top.funct7, test[4])
            ctx.set(top.immediate, test[5])

            await ctx.delay(Period(us=1))

            if ctx.get(top.result) != test[6]:
                err["has_error"] = True
                err["actual_result"] = ctx.get(top.result)

        sim.add_testbench(bench)
        return sim



    for i, test in enumerate(TESTS):
        error["has_error"] = False

        sim = create_bench(test, error)
        sim.run()

        if i % 1000 == 0:
            print(f"{i}/{total_tests} tests has been simulated.")
        if error["has_error"]:
            print(f"{i}/{total_tests} failed test!")
            print_test_details(test, error["actual_result"])
            
            sim = create_bench(test, error)

            filename = f"test_{i}.vcd"
            with sim.write_vcd(f"test_results/ALU/{filename}"):
                sim.run()
            
            print(f"See VCD {filename!r}.")
            if return_at_first_error:
                print("A test has failed. Stopping tests.")
                return
    
    # Can't bother to make this work in the loop
    print(f"{total_tests}/{total_tests} tests has been simulated.")
    print("All tests has finished!")

def get_alu_tests():
    return {
        "results_dir": TEST_RESULTS_DIR,
        "test_function": alu_tests
    }