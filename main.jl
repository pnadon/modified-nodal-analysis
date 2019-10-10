using CSV, DataFrames, Plots, Distributed, SparseArrays

df = CSV.File("./data/circuit.csv") |> DataFrame!

println(df)

[0:0.1:100;] |> x -> tan.(x) |> plot

array = Array{Float64}(undef, 5, 5)

sarray = spzeros(5, 5)

sarray[1, 1] = 5

sarray
