from agents import Agent , Runner , RunContextWrapper , function_tool , trace
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
import rich

load_dotenv()

# ------------------ Exercise 2 ------------------ #
#Airline Seat Preference Agent (Intermediate-Advanced)
#Requirement: Build a dynamic instructions system for an airline booking agent that customizes responses based on seat_preference and travel_experience.
#Window + First-time: Explain window benefits, mention scenic views, reassure about flight experience Middle + Frequent: Acknowledge the compromise, suggest strategies, offer alternatives Any + Premium: Highlight luxury options, upgrades, priority boarding
#Context Fields: seat_preference (window/aisle/middle/any), travel_experience (first_time/occasional/frequent/premium)

from agents import Agent, Runner, RunContextWrapper, function_tool, trace
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

load_dotenv()

# ------------------ Airline Seat Preference Agent ------------------ #

class SeatQuery(BaseModel):
    seat_preference: str  # window/aisle/middle/any
    travel_experience: str  # first_time/occasional/frequent/premium


# Example context
traveler = SeatQuery(
    seat_preference="window",
    travel_experience="first_time"
)

# Dynamic Instructions
async def airline_dynamic_instructions(ctx: RunContextWrapper[SeatQuery], agent: Agent):
    seat = ctx.context.seat_preference.lower()
    exp = ctx.context.travel_experience.lower()

    # Window + First-time
    if seat == "window" and exp == "first_time":
        return """
        A window seat is a great choice! You'll enjoy scenic views during takeoff, 
        flight, and landing. Since it's your first time flying, don't worry—it's normal 
        to feel excited or nervous. Just relax, enjoy the view, and the crew will 
        support you throughout the journey.
        """

    # Middle + Frequent
    elif seat == "middle" and exp == "frequent":
        return """
        A middle seat may not be the most comfortable, but as a frequent traveler, 
        you probably know strategies—like boarding early, using neck pillows, and 
        requesting aisle upgrades if available. Consider checking with the airline 
        for last-minute seat changes.
        """

    # Any + Premium
    elif seat == "any" and exp == "premium":
        return """
        Since you’re a premium traveler, you can choose from luxury seating options. 
        Enjoy spacious legroom, priority boarding, premium lounges, and even 
        complimentary upgrades depending on your airline's loyalty program. 
        Comfort and service are guaranteed!
        """

    # Default Fallback
    else:
        return f"""
        For your preference ({seat}) and travel experience ({exp}), the system 
        will provide tailored seat suggestions. Please check with the airline for 
        the best available options.
        """


# Create the agent
airline_agent = Agent(
    name="AirlineSeatAgent",
    instructions=airline_dynamic_instructions,
)

# Runner
async def main():
    with trace("Airline Seat Preference"):
        result = await Runner.run(
            airline_agent,
            "Help me choose a seat for my flight.",
            run_config=config,
            context=traveler
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
