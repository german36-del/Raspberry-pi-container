FROM ros:noetic
#Siempre empezamos con el FROM

#Para correr comandos utilizamos RUN. En este caso queremos instalar nano.
RUN apt-get update && apt-get install -y nano && rm -rf /var/lib/apt/lists/*

#Para copiar nuestros propios archivos en la imagen.
#Copiamos un archivo en un directorio de la imagen
COPY /git_repo/ /repositorio/

#Para solucionar el problema de los permisos, vamos a crear un usuario dentro de la imagen del sistema.
#Primero definiremos unos argumentos:

ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#Tras esto, creamos el usuario que no es root:
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config

#Codigo que se ejecuta como root

RUN apt-get update \
    #Primero instalamos sudo
    && apt-get install -y sudo \
    #Configuramos los privilegios de sudo para un usuario (USERNAME) y evitamos que pida la contrasenia cada vez que ejecutemos sudo
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

