# recipe-app-api
Recipe app api source code.

## Adding a new SSH key to your GitHub account
*Here's a [website](https://docs.github.com/en/enterprise-server@3.0/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to a simple guide*

#### Using GitHub.com
1. Copy the SSH public key to your clipboard.

*If your SSH public key file has a different name than the example code, modify the filename to match your current setup. When copying your key, don't add any newlines or whitespace.*

```bash
$ cat ~/.ssh/id_ed25519.pub
# Then select and copy the contents of the id_ed25519.pub file
# displayed in the terminal to your clipboard
```
2. In the upper-right corner of any page, click your profile photo, then click Settings.

3. In the user settings sidebar, click SSH and GPG keys.

4. Click New SSH key or Add SSH key.

5. In the "Title" field, add a descriptive label for the new key. For example, if you're using a personal Mac, you might call this key "Personal MacBook Air".

6. Paste your key into the "Key" field.

7. Click Add SSH key.

8. If prompted, confirm your GitHub Enterprise Server password.

#### Using GitHub CLI
1. To add an SSH key to your GitHub account, use the ssh-key add subcommand, specifying your public key.

``` bash
gh ssh-key add key-file
```

2. To include a title for the new key, use the -t or --title flag.

``` bash
gh ssh-key add key-file --title "personal laptop"
```

## Starting GitHub project
*Note that before starting a new project the SSH connection between GitHub and your computer have to be set*

1. Start by heading over to [GitHub](github.com) and just click on **new** button which takes you to the page that allows you to create a new repository.

2. Customize your repository:
* Give your repository the name.
* Give it the description.
* You can choose to initialize your project with **README** file.
* Check the *gitignore* file and choose **Python**.
* For the license you can choose a *MIT license*.

3. When you're done click *create repository* and what this will do is create a repository and take you to the repository page.

4. Once you're on the repository page click on *code* and then click a copy icon to copy the SSH link of the repository URL to your clipboard.

5. Launch terminal, move to your project's folder and type

``` bash
git clone <YOUR REPOSITORY SSH URL>
```
