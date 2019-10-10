using Base.Threads

function getInput()
    println("Enter start, end, n")
    collect([parse(Int64, x) for x in split(readline())])
end

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

function main()
    a, b, n = getInput()
    h = (b - a) / n

    n_threads = nthreads()
    total = Atomic{Float64}(0)
    local_n::Int64 = div(n, n_threads)
    @threads for rank in 0:n_threads - 1
        local_a = a + rank * local_n * h
        local_b = local_a + local_n * h
        local_ans = trap(local_a, local_b, local_n, h)
        println("local_a = $local_a, local_b = $local_b, ans = $local_ans")
        atomic_add!(total, local_ans)
    end

    println("the answer for a = $a, b = $b, n = $n: $(total[])")
end

main()
