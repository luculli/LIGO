## -- LAL case
## -------------------------------
IMAGE_NAME:=seagull/lal
CONTAINER_NAME:=lal
DOCKERFILE_NAME:=docker/Dockerfile

build-image:
	docker build --rm -t $(IMAGE_NAME) -f $(DOCKERFILE_NAME) .

start-image:
	exec docker run -d -it --gpus all -v $(CURDIR):/home/user  -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/.Xauthority:/home/user/.Xauthority:rw -v $(CURDIR)/src:/home/user/src -v $(CURDIR)/data:/home/user/data --net=host -e DISPLAY=$(DISPLAY) --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

run-image:
	exec docker run -it --gpus all -v $(CURDIR):/home/user  -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/.Xauthority:/home/user/.Xauthority:rw -v $(CURDIR)/src:/home/user/src -v $(CURDIR)/data:/home/user/data --net=host -e DISPLAY=$(DISPLAY) --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

run-bash:
	exec docker run -it --gpus all -v $(CURDIR):/home/user  -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/.Xauthority:/home/user/.Xauthority:rw -v $(CURDIR)/src:/home/user/src -v $(CURDIR)/data:/home/user/data --net=host -e DISPLAY=$(DISPLAY) --rm --name $(CONTAINER_NAME) $(IMAGE_NAME) /bin/bash

stop-image:
	docker stop $(CONTAINER_NAME)

remove-image:
	docker rm $(IMAGE_NAME)
