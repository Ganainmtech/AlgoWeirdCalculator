# Importing beaker and pyteal
import beaker as bk
import pyteal as pt


class MyState:
    # variable set equal to the global state value where it is a number
    result = bk.GlobalStateValue(pt.TealType.uint64)


# Creating application with name Calculator
app = bk.Application("Calculator", state=MyState())  # Has access to MyState class


# Exposing add method to ABI, so front end knows how to call this method
@app.external
# Method stores an takes 2 arg's on the left, outputs on the right
def add(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    add_result = a.get() + b.get()
    # Returns a sequence
    return pt.Seq(
        # Set add_result value to the result state defined in MyClass
        app.state.result.set(add_result),
        output.set(add_result),
    )


@app.external(read_only=True)
# Mothod that reads the state and outputs a uint64 type (number)
def read_result(*, output: pt.abi.Uint64) -> pt.Expr:
    # Returns application state result
    return output.set(app.state.result)


if __name__ == "__main__":
    # Build out app compile beaker and pyteal code into TEAL Code
    app.build().export("./artifacts")
