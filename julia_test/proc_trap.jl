using Base.Threads
using Distributed
@everywhere include("Trap.jl")

function getInput()
    println("Enter start, end, n")
    collect([parse(Int64, x) for x in split(readline())])
end

function main(a=0, b=131072, n=32768)
    # a, b, n = getInput()
    h = (b - a) / n

    n_threads = nprocs()
    if n_threads == 1
        println("
        Number of threads detected to be =1\n
        environment variables may not be properly set up!\n
        exiting..."
        )
        return
    end
    workers = Array{Future}(undef, n_threads - 1)
    total = 0
    local_n::Int64 = div(n, n_threads - 1)
    for rank in 2:n_threads
        local_a = a + (rank + 1) * local_n * h
        local_b = local_a + local_n * h
        # println("at $rank: local_a = $local_a, local_b = $local_b")
        workers[rank - 1] = @spawnat rank Trap.trap(local_a, local_b, local_n, h)
    end

    for rank in 2:n_threads
        local_ans = fetch(workers[rank - 1])
        # println("at $rank: ans = $local_ans")
        total += local_ans
    end

    # println("the answer for a = $a, b = $b, n = $n: $(total[])")
end

for i=1:10000
    main()
end