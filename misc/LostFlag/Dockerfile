FROM alpine:latest

ENV USER hackiit
ENV PSWD LSExf8pbM8c8QZXm
ENV FLAG ETSIIT_CTF{PlayingWithTheShellIsAlwaysFun!!!}

# Install bash and openssh-server and clean
RUN apk update \
	&& apk add --no-cache --upgrade bash openssh-server \
	&& rm -rf /var/lib/{cache,log}/ \
	&& rm -rf /var/lib/apt/lists/*.lz4 \
	&& rm -rf /var/log/* \
	&& rm -rf /tmp/* /var/tmp/* \
	&& rm -rf /usr/share/doc/ \
	&& rm -rf /usr/share/man/ \
	&& rm -rf /var/cache/apk/* \
	&& ssh-keygen -A

# Allow only rbash from SSH
RUN echo "PATH=" > /bin/rbash_script
RUN echo 'if [ "$SSH_ORIGINAL_COMMAND" ]; then echo ":(" >&2; exit 1; else /bin/rbash; fi' >> /bin/rbash_script
RUN chmod +x /bin/rbash_script
RUN echo "ForceCommand    rbash_script" >> /etc/ssh/sshd_config 
RUN ln -s /bin/bash /bin/rbash

# Create user account
RUN adduser ${USER} -s /bin/rbash;echo "${USER}:${PSWD}" | chpasswd

# Configuration for rbash
RUN echo "PATH=" > /home/${USER}/.bash_profile
RUN chown root:root /home/${USER}/.bash_profile
RUN chmod 444 /home/${USER}/.bash_profile
RUN chattr +i /home/${USER}/.bash_profile
RUN echo 'unset HISTFILE' >> /etc/profile.d/custom.sh
RUN echo "PS1='🚩🚩🚩: '" >> /etc/profile.d/custom.sh

# Generate flags
RUN echo "'Oopsie, wrong flag!'" > /home/${USER}/.flag
RUN echo ${FLAG} > /home/${USER}/.flag⠀

# Expose SSH port
EXPOSE 22/tcp

# Start SSH daemon 
CMD ["/usr/sbin/sshd", "-p", "2222", "-D"]