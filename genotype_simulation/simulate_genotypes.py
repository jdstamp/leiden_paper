import stdpopsim
import msprime


def simulate():
    n_samples = 1000
    sequence_length = 100000000
    file_prefix = "stdpopsim"
    species = stdpopsim.get_species("HomSap")
    demo = species.get_demographic_model("AmericanAdmixture_4B11")
    ts = msprime.sim_ancestry(
        samples=[
            msprime.SampleSet(n_samples, ploidy=2, population="AFR"),  # pop id 0
            msprime.SampleSet(n_samples, ploidy=2, population="EUR"),
            msprime.SampleSet(n_samples, ploidy=2, population="ASIA"),
            msprime.SampleSet(n_samples, ploidy=2, population="ADMIX"),  # pop id 3
        ],
        demography=demo.model,
        sequence_length=sequence_length,
        recombination_rate=1e-8,
        random_seed=42,
    )
    mts = msprime.sim_mutations(
        tree_sequence=ts,
        rate=1.5e-8,
        model="jc69",
        random_seed=42,
        discrete_genome=False,
    )
    individual_names = []
    for pop in demo.model.populations:
        pop_names = [f"{pop.name}_{i:04d}" for i in range(n_samples)]
        individual_names += pop_names
    with open(f"{file_prefix}.vcf", "w") as file:
        mts.write_vcf(file, individual_names=individual_names)


if __name__ == "__main__":
    simulate()
