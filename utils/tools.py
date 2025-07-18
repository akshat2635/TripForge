import os
from langchain_core.tools import tool
from serpapi import GoogleSearch
from typing import Optional

@tool
def search_flights(
    departure_city: str,
    arrival_city: str,
    departure_date: str,
    adults: int = 1,
    children: int = 0,
    currency: str = "INR",
    travel_class: int = 1,          # 1: Economy, 2: Premium economy, 3: Business, 4: First
    deep_search: bool = False,      # Enable full-depth search from Google Flights
    sort_by: int = 1,               # 1: Top, 2: Price, 3: Departure, 4: Arrival, 5: Duration, 6: Emissions
) -> str:
    """
    Search flights using SerpAPI Google Flights engine.

    Args:
        departure_city: Departure city IATA code (e.g., "DEL" for Delhi)
        arrival_city: Arrival city IATA code (e.g., "GOI" for Goa)
        departure_date: Departure date in YYYY-MM-DD format
        adults: Number of adults (default: 1)
        children: Number of children (default: 0)
        currency: Currency code (default: "INR")
        travel_class: 1 - Economy (default), 2 - Premium economy, 3 - Business, 4 - First
        deep_search: Set to true for deep Google-style search (default: False)
        sort_by: Sorting mode (1: Top, 2: Price, 3: Departure, 4: Arrival, 5: Duration, 6: Emissions)
        
    Returns:
        String containing flight search results
    """
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY not found in environment variables"
    adults = int(adults)
    children = int(children)
    travel_class = int(travel_class)
    sort_by = int(sort_by)
    params = {
        "engine": "google_flights",
        "departure_id": departure_city,
        "arrival_id": arrival_city,
        "outbound_date": departure_date,
        "adults": str(adults),
        "children": str(children),
        "currency": currency,
        "gl": "in",
        "hl": "en",
        "type": "2",
        "api_key": api_key,
        "travel_class": str(travel_class),
        "deep_search": str(deep_search).lower(),
        "sort_by": str(sort_by)
    }


    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        # print(f"Search results: {results}")  # Debugging line to check results

        flight_pool = []
        if 'best_flights' in results and results['best_flights']:
            flight_pool = results['best_flights'][:3]
        elif 'other_flights' in results and results['other_flights']:
            flight_pool = results['other_flights'][:3]  

        if not flight_pool:
            return f"No flights found from {departure_city} to {arrival_city} on {departure_date}"
        
        flight_info = []

        for idx, flight in enumerate(flight_pool):
            legs = flight.get('flights', [])
            layovers = flight.get('layovers', [])
            total_duration = flight.get('total_duration', 'Unknown')
            price = flight.get('price', 'Price not available')
            flight_type = flight.get('type', 'Unknown')
            departure_token = flight.get('departure_token', 'N/A')
            airline_logo = flight.get('airline_logo', 'N/A')

            # Build string for each leg
            flight_legs_info = []
            for i, leg in enumerate(legs):
                airline = leg.get('airline', 'Unknown Airline')
                flight_number = leg.get('flight_number', 'N/A')
                travel_class = leg.get('travel_class', 'N/A')

                dep_airport_info = leg.get('departure_airport', {})
                arr_airport_info = leg.get('arrival_airport', {})
                departure_airport = dep_airport_info.get('name', 'Unknown')
                departure_id = dep_airport_info.get('id', 'N/A')
                departure_time = dep_airport_info.get('time', 'Unknown')

                arrival_airport = arr_airport_info.get('name', 'Unknown')
                arrival_id = arr_airport_info.get('id', 'N/A')
                arrival_time = arr_airport_info.get('time', 'Unknown')

                duration = leg.get('duration', 'Unknown')

                leg_info = (
                    f"  Leg {i+1}:\n"
                    f"    Airline: {airline} ({flight_number})\n"
                    f"    Class: {travel_class}\n"
                    f"    From: {departure_airport} ({departure_id}) at {departure_time}\n"
                    f"    To: {arrival_airport} ({arrival_id}) at {arrival_time}\n"
                    f"    Duration: {duration} mins"
                )
                flight_legs_info.append(leg_info)

            # Layovers
            layover_info = []
            for j, layover in enumerate(layovers):
                layover_name = layover.get("name", "Unknown airport")
                layover_duration = layover.get("duration", "Unknown")
                overnight = " (overnight)" if layover.get("overnight") else ""
                layover_info.append(f"  Layover {j+1}: {layover_name}, Duration: {layover_duration} mins{overnight}")

            full_flight_info = (
                f"Flight Option {idx+1}:\n"
                + "\n".join(flight_legs_info)
                + ("\n" + "\n".join(layover_info) if layover_info else "")
                + f"\n  Total Duration: {total_duration} mins"
                + f"\n  Price: {price}"
                + f"\n  Type: {flight_type}"
                + f"\n  Airline Logo: {airline_logo}"
                + f"\n  Departure Token: {departure_token}\n"
                + "-" * 50
            )

            flight_info.append(full_flight_info)

        return "\n".join(flight_info)

        
    except Exception as e:
        return f"Error searching flights: {str(e)}"


@tool
def search_hotels(
    query: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 2,
    children: int = 0,
    sort_by: Optional[int] = None,
    currency: str = "INR",
    rating: Optional[int] = None,
    hotel_class: Optional[str] = None
) -> str:
    """
    Search hotels using SerpAPI Google Hotels engine.

    Args:
        query: Location to search for hotels (e.g., "Goa, India")
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        adults: Number of adults (default: 2)
        children: Number of children (default: 0)
        sort_by: Sorting mode (3: Lowest price, 8: Highest rating, 13: Most reviewed)
        currency: Currency code to display prices in (default: "INR")
        rating: Minimum rating filter (7: 3.5+, 8: 4.0+, 9: 4.5+)
        hotel_class: Filter by hotel star class (e.g., "3", "4", or "3,4,5" for multiple)

    Returns:
        String containing formatted hotel search results, including name, rating, price per night,
        amenities, coordinates, image, and booking link
    """

    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY not found in environment variables"
    adults = int(adults)
    children = int(children)
    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "children": children,
        "currency": currency,
        "gl": "in",
        "hl": "en",
        "api_key": api_key
    }
    
    if sort_by is not None:
        params["sort_by"] = sort_by
    if rating is not None:
        params["rating"] = rating
    if hotel_class is not None:
        params["hotel_class"] = hotel_class

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'properties' not in results:
            return f"No hotels found for {query} from {check_in_date} to {check_out_date}"
        
        hotels = results['properties'][:3]  # Limit to top 3
        hotel_info = []

        for hotel in hotels:
            name = hotel.get('name', 'Unknown Hotel')
            type_ = hotel.get('type', 'Unknown Type')
            rating = hotel.get('overall_rating', 'No rating')
            reviews = hotel.get('reviews', 'N/A')
            price = hotel.get('rate_per_night', {}).get('lowest', 'N/A')
            taxes = hotel.get('rate_per_night', {}).get('before_taxes_fees', 'N/A')
            price_guests = hotel.get('prices', [{}])[0].get('num_guests', adults)
            source = hotel.get('prices', [{}])[0].get('source', 'N/A')
            logo = hotel.get('prices', [{}])[0].get('logo', 'N/A')
            property_token = hotel.get('property_token', 'N/A')
            link = hotel.get('link', hotel.get('serpapi_property_details_link', 'N/A'))
            coords = hotel.get('gps_coordinates', {})
            lat = coords.get('latitude', 'N/A')
            lon = coords.get('longitude', 'N/A')
            check_in = hotel.get('check_in_time', 'N/A')
            check_out = hotel.get('check_out_time', 'N/A')
            essential = ', '.join(hotel.get('essential_info', []))
            amenities = ', '.join(hotel.get('amenities', []))
            excluded = ', '.join(hotel.get('excluded_amenities', []))
            image = hotel.get('images', [{}])[0].get('original_image', 'N/A')

            nearby_places = []
            for place in hotel.get("nearby_places", []):
                place_name = place.get("name")
                transports = [f"{t['type']} ({t['duration']})" for t in place.get("transportations", [])]
                nearby_places.append(f"{place_name} - {'; '.join(transports)}")
            nearby_summary = "; ".join(nearby_places) if nearby_places else "None"

            hotel_info.append(
                f"Hotel: {name} ({type_})\n"
                f"Rating: {rating} ({reviews} reviews)\n"
                f"Price per night for {price_guests} guests: {price} (Before taxes: {taxes}) via {source}\n"
                f"Amenities: {amenities}\n"
                f"Excluded Amenities: {excluded}\n"
                f"Essential Info: {essential}\n"
                f"Location: Latitude {lat}, Longitude {lon}\n"
                f"Check-in Time: {check_in}, Check-out Time: {check_out}\n"
                f"Nearby Places: {nearby_summary}\n"
                f"Booking Link: {link}\n"
                f"Property Token: {property_token}\n"
                f"Image: {image}\n"
                f"Source Logo: {logo}\n"
                "-------------------------------------------"
            )

        return "\n".join(hotel_info)

    except Exception as e:
        return f"Error searching hotels: {str(e)}"


def save_itinerary(filename: str, itinerary: str) -> str:
    """
    Save the generated itinerary to a file.

    Args:
        filename: Name of the file to save the itinerary
        itinerary: Itinerary content as a string

    Returns:
        Confirmation message
    """
    filename = "data/" + filename
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(itinerary)
        return f"Itinerary saved successfully to {filename}."
    except Exception as e:
        return f"Error saving itinerary: {str(e)}"

def save_preferences(preferences: str, filename: str) -> str:
    """
    Save user preferences to a file.

    Args:
        preferences: JSON string containing user preferences

    Returns:
        Confirmation message
    """
    filename = "data/" + filename
    try:
        with open(filename, "w") as f:
            f.write(preferences)
        return "Preferences saved successfully."
    except Exception as e:
        return f"Error saving preferences: {str(e)}"

tools = [search_flights, search_hotels]
tools_dict = {tool.name: tool for tool in tools}