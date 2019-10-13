module Trap
export trap

function trap(
    left_endpt::Float64,
    right_endpt::Float64,
    trap_count::Int64,
    base_len::Float64)

    f(x) = x^2

    estimate = (f(left_endpt) + f(right_endpt)) / 2.0
    for i=1:trap_count - 1
        estimate += f(left_endpt + i * base_len) # type instability
    end
    return estimate * base_len
end
end
