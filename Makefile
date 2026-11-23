.PHONY: test-local base images up run-seeds kind deploy regress clean
test-local:            ## run cocotb directly (needs iverilog + cocotb installed)
	cd tb && make -f Makefile.cocotb
base:
	docker build -t vlsi-eda-base:latest -f docker/eda-base/Dockerfile .
images: base
	docker build -t vlsi-runner:latest -f docker/runner/Dockerfile .
	docker build -t vlsi-controller:latest -f docker/controller/Dockerfile .
	docker build -t vlsi-dashboard:latest -f docker/dashboard/Dockerfile .
up:
	docker compose up -d postgres minio controller dashboard
run-seeds:
	for s in 1 2 3 4; do docker compose run --rm -e SEED=$$s runner & done; wait
kind:
	./scripts/kind-setup.sh
deploy:
	kubectl apply -k k8s/overlays/dev
regress:
	./scripts/submit_regression.sh
clean:
	rm -rf tb/sim_build* tb/results*.xml tb/*.fst
