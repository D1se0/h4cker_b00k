---
icon: briefcase
---

# Entorno de trabajo (Kali Linux)

URL = [GitHub ohmyzsh](https://github.com/ohmyzsh/ohmyzsh)

Por lo que en nuestra terminal vamos a ejecutar lo siguiente:

```shell
sh -c "$(curl -fsSL
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Esto nos instalara de forma automatica `ohmyzsh` y veremos lo siguiente:

```
Looking for an existing zsh config...
Found /home/kali/.zshrc. Backing up to /home/kali/.zshrc.pre-oh-my-zsh
Using the Oh My Zsh template file and adding it to /home/kali/.zshrc.

         __                                     __   
  ____  / /_     ____ ___  __  __   ____  _____/ /_  
 / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \ 
/ /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / / 
\____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/  
                        /____/                       ....is now installed!


Before you scream Oh My Zsh! look over the `.zshrc` file to select plugins, themes, and options.

• Follow us on X: https://x.com/ohmyzsh
• Join our Discord community: https://discord.gg/ohmyzsh
• Get stickers, t-shirts, coffee mugs and more: https://shop.planetargon.com/collections/oh-my-zsh

➜  ~ 
```

Ahora ejecutaremos lo siguiente para que no nos aparezca este comando continuamente:

```shell
touch ~/.hushlogin
```

Esto solo se centra en el binario de `python`.

Ahora lo que vamos hacer es instalar algunos `temas` y `plugins` a nuestra terminal.

En el siguiente repositorio estaran las instrucciones para poner nuestro `prompt` de mejor manera:

URL = [GitHub powerlevel10k](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#im-using-powerlevel9k-with-oh-my-zsh-how-do-i-migrate)

Por lo que ejecutaremos lo siguiente:

```shell
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

Ahora vamos a modificar el siguiente fichero llamado `.zshrc`:

```shell
nano .zshrc

#Dentro del nano
#Cambiaremos esta linea:
#ZSH_THEME="robbyrussell"
#Por esto de aqui:
ZSH_THEME="powerlevel10k/powerlevel10k"
```

Ahora una vez guardado, cerraremos la terminal y la volveremos abrir, veremos lo siguiente:

```
This is Powerlevel10k configuration wizard. You are seeing it because you haven't
  defined any Powerlevel10k configuration options. It will ask you a few questions and
                                 configure your prompt.

                    Does this look like a diamond (rotated square)?
                      reference: https://graphemica.com/%E2%97%86

                                     --->    <---

(y)  Yes.

(n)  No.

(q)  Quit and do nothing.

Choice [ynq]:
```

En estas preguntas tendremos que responder si estamos viendo lo que realmente aparece entre las flechas, para que nos lo configure bien, en mi caso pondre `y`, y asi continuamente hasta terminal el cuestionario.

Una vez terminado ya veremos el `prompt` que hemos configurado.

Ahora vamos a cambiar una configuracion la cual sera del siguiente fichero:

```shell
nano ~/.p10k.zsh

#Dentro del nano
#Cambiaremos la siguiente configuracion comentando las siguientes lineas:
#status                  # exit code of the last command
    #command_execution_time  # duration of the last command
    #background_jobs         # presence of background jobs
    #direnv                  # direnv status (https://direnv.net/)
    #asdf                    # asdf version manager (https://github.com/asdf-vm/asdf)
    #virtualenv              # python virtual environment (https://docs.python.org/3/library/venv.html)
    #anaconda                # conda environment (https://conda.io/)
    #pyenv                   # python environment (https://github.com/pyenv/pyenv)
    #goenv                   # go environment (https://github.com/syndbg/goenv)
    #nodenv                  # node.js version from nodenv (https://github.com/nodenv/nodenv)
    #nvm                     # node.js version from nvm (https://github.com/nvm-sh/nvm)
    #nodeenv                 # node.js environment (https://github.com/ekalinin/nodeenv)
#rbenv                   # ruby version from rbenv (https://github.com/rbenv/rbenv)
    #rvm                     # ruby version from rvm (https://rvm.io)
    #fvm                     # flutter version management (https://github.com/leoafarias/fvm)
    #luaenv                  # lua version from luaenv (https://github.com/cehoffman/luaenv)
    #jenv                    # java version from jenv (https://github.com/jenv/jenv)
    #plenv
#perlbrew                # perl version from perlbrew (https://github.com/gugod/App-perlbrew)
    #phpenv                  # php version from phpenv (https://github.com/phpenv/phpenv)
    #scalaenv                # scala version from scalaenv (https://github.com/scalaenv/scalaenv)
    #haskell_stack           # haskell version from stack (https://haskellstack.org/)
    #kubecontext             # current kubernetes context (https://kubernetes.io/)
    #terraform               # terraform workspace (https://www.terraform.io)
    # terraform_version     # terraform version (https://www.terraform.io)
    #aws                     # aws profile (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
    #aws_eb_env              # aws elastic beanstalk environment (https://aws.amazon.com/elasticbeanstalk/)
    #azure                   # azure account name (https://docs.microsoft.com/en-us/cli/azure)
    #gcloud                  # google cloud cli account and project (https://cloud.google.com/)
    #google_app_cred         # google application credentials (https://cloud.google.com/docs/authentication/production)
    #toolbox                 # toolbox name (https://github.com/containers/toolbox)
    #context                 # user@hostname
    #nordvpn                 # nordvpn connection status, linux only (https://nordvpn.com/)
    #ranger                  # ranger shell (https://github.com/ranger/ranger)
    #yazi                    # yazi shell (https://github.com/sxyazi/yazi)
    #nnn                     # nnn shell (https://github.com/jarun/nnn)
    #lf                      # lf shell (https://github.com/gokcehan/lf)
    #xplr                    # xplr shell (https://github.com/sayanarijit/xplr)
    #vim_shell               # vim shell indicator (:sh)
    #midnight_commander      # midnight commander shell (https://midnight-commander.org/)
    #nix_shell               # nix shell (https://nixos.org/nixos/nix-pills/developing-with-nix-shell.html)
    #chezmoi_shell           # chezmoi shell (https://www.chezmoi.io/)
    #vi_mode                 # vi mode (you don't need this if you've enabled prompt_char)
#todo                    # todo items (https://github.com/todotxt/todo.txt-cli)
    #timewarrior             # timewarrior tracking status (https://timewarrior.net/)
    #taskwarrior             # taskwarrior task count (https://taskwarrior.org/)
    #per_directory_history   # Oh My Zsh per-directory-history local/global indicator
#Ahora descomentar lo siguiente:
ip
#Comentamos en la parte superior lo siguiente:
#vcs                     # git status
#En la misma linea añadimos lo siguiente:
status                  # exit code of the last command
```

Ahora si lo guardamos, cerramos la terminal y la volvemos abrir, veremos que se aplico correctamente mostrando la informacion necesaria, pero manteniendolo minimalista.

Ahora vamos a instalar algun `plugins` los cuales nos ayudan a resaltar los comandos del sistema y a recordar los comandos que ejecutamos anteriormente.

Nos iremos al siguiente link para instalarlo:

URL = [GitHub zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)

Ejecutamos el siguiente comando en la terminal:

```shell
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Ahora antes de modificar el fichero `.zshrc` instalaremos el otro `plugin` que el anterior es para resaltar los comandos del sistema y este siguiente para recordarlos.

URL = [GitHub zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md)

Ejecutaremos el siguiente comando:

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Ahora tendremos que dejar la siguiente linea como esta en el archivo `.zshrc`:

```shell
sudo nano .zshrc

#Dentro del nano
plugins=(
   git
   zsh-autosuggestions
   zsh-syntax-highlighting
)
```

Guardamos y cerramos la terminal, la volvemos abrir y probamos a poner lo siguiente:

```shell
echo "Hola"
```

Vemos que nos esta detectando el comando y si volvemos a ponerlo nos lo recuerda.
