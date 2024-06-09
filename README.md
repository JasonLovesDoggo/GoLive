![Title.png](https://cdn.dorahacks.io/static/files/18ffd3d73d8bf23018d13d84b95ae9f0.png)

# Inspiration
We have been to many hackathons, and one challenge every developer has faced is deploying their application. Whether it’s beginners doing it for the first time, or experienced developers switching to another framework, the hassle of looking through documentation is constant. Instead of relearning the process with every framework and every language, we have created a streamlined process with GoLive!

# What it does
GoLive automates the entire deployment process. It first detects what type of app your site is, pops open a config site so you can override defaults and chooses deployment location (including bare metal - e.g. Raspberry Pi). Then, it automagically dockerizes it and uses OpenTofu (Terraform) to deploy your site to the provider of your choice. Lastly, it walks you through setting your DNS records so you can view your site on your domain instead of 192.329.329.32:3203 (like I'm not remembering that).

![Deploy.png](https://cdn.dorahacks.io/static/files/18ffd3c5747c089383785714895904fb.png)

# How we built it 
Starting from the design, we created low fidelity wireframes of the dashboard and website, then used a combination of Figma and Adobe Photoshop to design the website and assets.
For the front end, we used HTML and CSS and integrated it with the back end using Flask.
For the backend, we used Python, Docker, OpenTofu (a fork of Terraform), and bash along with micro bits of code from Rust, Go, Perl, PHP, JavaScript & more

![TechFlow.png](https://cdn.dorahacks.io/static/files/18ffd3cf873c47be456b55c4ff1913da.png)

![LowFidelity.jpg](https://cdn.dorahacks.io/static/files/18ffd420ad00ba828abb6d44381acc02.jpg)

# Challenges we ran into 

Getting OpenTofu set up and configured was a massive struggle, to the point that we were considering giving up and hardcoding it. But luckily, after around 14 hrs of straight debugging, it WORKED! Our issue turned out to be a simple missing config part which was only four lines of code but turned into a whole rabbit hole of never-ending errors. After a whole lot of trial and error and two rewrites of the config, it worked.  

# Accomplishments that we're proud of

We're super proud of the UI and specifically the icon (We love GOphernaut!!)

Other than that, we're super proud/amazed how GoLive can deploy itself, it can fully dockerize it so you can run it on any machine without having to bother with external steps. 

In addition, we can support 10 languages and 8 frameworks so it's awesome how much our code can do.

# What we've learned
~~Don't do a DevOps automation project within 36hrs, it hurts~~
### Jason
This was my first time using IoC or CoC so this was honestly quite a challenge. Between NixOS, ansible, terraform or other related tools, it was just as much of a challenge to choose the tools as implement them.
In the end, I went with Terraform and somehow managed to get a working product!

### Nico
This was my first time using Flask and Google Cloud services.

### Lin
I have never delved so deeply into a single tag type in HTML before until now. We wanted to get the directory of a file the user uploads, which uses the input tag as the file type. I learned that under normal conditions, web browsers don’t allow access to the full location of a file unless a flag is used. 

# What's next for GoLive!
There are a couple of big new features that are lined up.
- More cloud providers/languages/frameworks:
 - Given how our system is structured, we can easily support new systems with just a template or two added.
- Auto-scaling capabilities 
- Ability to manage (redeploy or undeploy) previous projects.

# Figma Links
[Deployment Page](https://www.figma.com/proto/szC41XCiFChewEI9XV8nio/Untitled?node-id=2-10&t=aiqZzMmwGWl1dIAL-1&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=2%3A10&show-proto-sidebar=1)
[Static Website](https://www.figma.com/proto/szC41XCiFChewEI9XV8nio/Untitled?node-id=5-8&t=aiqZzMmwGWl1dIAL-1&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=5%3A8&show-proto-sidebar=1)
[Dashboard](https://www.figma.com/proto/szC41XCiFChewEI9XV8nio/Untitled?node-id=9-73&t=aiqZzMmwGWl1dIAL-1&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=9%3A73&show-proto-sidebar=1)
[Slides](https://www.figma.com/proto/szC41XCiFChewEI9XV8nio/Untitled?node-id=61-178&t=aiqZzMmwGWl1dIAL-1&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=61%3A178&show-proto-sidebar=1)
[Demo video](https://drive.google.com/file/d/1pcrdJqgPRquZuSqky1ha3nKpKjUR8YbB/view?usp=sharing)

![StaticSite.png](https://cdn.dorahacks.io/static/files/18ffd3f4f0bdbf254d8cb0849d0a61ac.png)
