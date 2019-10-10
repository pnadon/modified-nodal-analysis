# double Trap(
#             double left_endpt,
#             double right_endpt,
#             int trap_count,
#             double base_len) {
#     double estimate, x;
#     int i;
#
#     estimate = (f(left_endpt) + f(right_endpt)) / 2.0;
#     for (i = 1; i <= trap_count - 1; i++) {
#         x = left_endpt + i * base_len;
#         estimate += f(x);
#     }
#     estimate = estimate * base_len;
#
#     return estimate;
# }
module Trap
export trap

function trap(
    left_endpt::Float64,
    right_endpt::Float64,
    trap_count::Int64,
    base_len::Float64)

    f(x) = x^2

    estimate = f(left_endpt) + f(right_endpt)) / 2.0
    for i=1..trap_count - 1
        estimate += f(left_endpt + i * base_len) # type instability
    end
    return estimate * base_len
end
end
