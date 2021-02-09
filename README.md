# mTree Auction Exmaples

The content of this repository will help to illustrate constructing various auctions in the mTree framework. 

# Running mTree with Docker

Running mTree with Docker is the easiest way to get started. 

1. In order to do this you will first want to download and install Docker on your system. You can find the appropriate version of Docker Desktop at https://www.docker.com/products/docker-desktop

2. After you've installed Docker and verified it works, you will need to pull down the appropriate image containing mTree. To do this you can look at the mTree docker images at: https://hub.docker.com/r/mtree/mtree . To pull this you will follow the directions and use the command prompt or terminal and type in: `docker pull mtree/mtree`. This will install the image on your system. You should then see the mTree image available in your Images section of the Docker Desktop app.

3. Now you'll want to ensure that you have cloned this mtree_auction_examples repository somewhere on your local machine. You can easily clonse this repository by going into the command prompt or terminal and typing `git clone https://github.com/gmucsn/mTree_auction_examples.git` . You will want to record the location of where you cloned the repository for later use.

4. Now you can configure your mTree image to launch and incorporate your cloned auction examples repository. This configuration step is important as it will allow you to run your Microeconomic System code inside mTree. To configure this, go into the Images area in docker desktop. There you will see the mTree image. You will also see a button that says "Run." If you click that it will bring up the New Container dialog box. You will see the optional settings area in this box. In the optional settings area you will need to setup the Volumes information. In the Host Path box click and find the auction examples repository folder. Then, in the Container Path box type in `/auctions`. Then hit run.

5. You will now be int he Container/Apps area of the Docker Desktop app. You will see a line that has a randomly generated name that is your mTree container. If you hover over the line several buttons on the right will appear. Click on the furthest to the left (when you hover over it it will say "CLI"). This will open up a command prompt or terminal. You will then be presented with a prompt that starts with "#". 

6. You are now in the mTree container. You will then type in the next commands to run a basic simulation.

7. Type in `cd /auctions/sealed_bid_common_value_auction/`. This will switch you to the example sealed bid common value auction MES.

8. Type in `mTree_runner -i ./config/basic_simulation.json`

9. You will now be int he mTree runner. Inside this you will type `run_simulation` to start running the auction code. 

10. You will be able to see the log files for your simulation in your mTree_auction_examples cloned repository folder.

# Auction Types

## Sealed Bid Common Value Auction

This will be a simple reference auction showing how an auction can be conducted. In particular, this will demonstrate a simple sealed bid common value auction.

## Double Auction

