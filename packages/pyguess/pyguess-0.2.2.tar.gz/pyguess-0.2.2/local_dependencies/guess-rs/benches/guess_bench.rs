use criterion::{black_box, criterion_group, criterion_main, Criterion};
use guess_rs::{addr, guessr::STREET_NAMES_FILE, *};

fn bench_street_matcher(c: &mut Criterion) {
    c.bench_function("Guess address with Location::Place", |b| {
        b.iter(|| {
            guessr::guess_address(
                black_box("ch de saint-cierges 3"),
                black_box(Location::Place("bercher".to_string())),
                black_box(Config::default()),
            )
        })
    });

    c.bench_function("Guess address with Location::Zip", |b| {
        b.iter(|| {
            guessr::guess_address(
                black_box("qu du seujet 36"),
                black_box(Location::Zip(1201)),
                black_box(Config::default()),
            )
        })
    });

    c.bench_function("Guess address with Location::Empty (street range)", |b| {
        b.iter(|| {
            guessr::guess_address(
                black_box("Mühlematt 7-11 (Emmenbrücke)"),
                black_box(Location::Empty),
                black_box(Config::default()),
            )
            .unwrap();
        })
    });

    c.bench_function(
        "Guess address with Location::Empty (missing two letters)",
        |b| {
            b.iter(|| {
                guessr::guess_address(
                    black_box("qu du seujet 36"),
                    black_box(Location::Empty),
                    black_box(Config::default()),
                )
                .unwrap()
            })
        },
    );

    c.bench_function(
        "Guess address with Location::Empty (missing first letter)",
        |b| {
            b.iter(|| {
                guessr::guess_address(
                    black_box("uai du seujet 36"),
                    black_box(Location::Empty),
                    black_box(Config::default()),
                )
                .unwrap()
            })
        },
    );

    c.bench_function("Search in file (default config)", |b| {
        let config = Config::default();
        b.iter(|| {
            guessr::search_in_candidates_file(
                black_box(&addr::clean_street("ch de saint-cierges 3,fas23dfsfsdf")),
                black_box(&config.path_to_streets.join(STREET_NAMES_FILE)),
                black_box(&config),
            )
            .unwrap()
        })
    });

    c.bench_function("Search in file (JaroWinkler)", |b| {
        b.iter(|| {
            let cfg = Config::new(0.6, 0.8, 100, StringMetric::JaroWinkler, None, None);
            guessr::search_in_candidates_file(
                black_box("ch de saint-cierges 3,fas23dfsfsdf"),
                black_box(&cfg.path_to_streets.join(STREET_NAMES_FILE)),
                black_box(&cfg),
            )
            .unwrap()
        })
    });

    c.bench_function("Search in file (Jaro)", |b| {
        b.iter(|| {
            let cfg = Config::new(0.5, 0.8, 500, StringMetric::Jaro, None, None);
            guessr::search_in_candidates_file(
                black_box("ch de saint-cierges 3"),
                black_box(&cfg.path_to_streets.join("street_names.txt")),
                black_box(&cfg),
            )
            .unwrap()
        })
    });
}

criterion_group!(benches, bench_street_matcher);
criterion_main!(benches);
