import matplotlib.pyplot as plt
from tabulate import tabulate

# Function to load driver data
def load_driver_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    race_location = lines[0].strip()
    lap_times = {}
    
    for line in lines[1:]:
        driver_code, lap_time = line[:3], float(line[3:])
        if driver_code not in lap_times:
            lap_times[driver_code] = []
        lap_times[driver_code].append(lap_time)
    
    return race_location, lap_times

# Function to load driver details from the driver data file
def load_driver_details(filename):
    driver_data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row = line.strip().split(',')
            driver_code = row[1]
            driver_data[driver_code] = {
                'ID': row[0],
                'Name': row[2],
                'Car': row[3]
            }
    return driver_data

def display_driver_details(driver_details):
    print("Driver Details:")
    formatted_details = {
        driver_code: f"ID: {details['ID']}, Name: {details['Name']}, CAR: {details['Car']}"
        for driver_code, details in driver_details.items()
    }
    print(tabulate(formatted_details.items(), headers=['Driver Code', 'Details'], tablefmt='grid'))
    print()


# Function to display race location
def display_race_location(race_location):
    print(f"Race Location: {race_location}\n")

# Function to find the fastest driver
def find_fastest_driver(lap_times):
    fastest_driver = None
    fastest_time = float('inf')
    for driver, times in lap_times.items():
        best_time = min(times)
        if best_time < fastest_time:
            fastest_time = best_time
            fastest_driver = driver
    
    return fastest_driver, fastest_time

# Function to calculate average lap time for each driver
def calculate_average_lap_times(lap_times):
    avg_times = {driver: sum(times) / len(times) for driver, times in lap_times.items()}
    return avg_times

# Function to calculate the overall average lap time
def calculate_overall_average_lap_time(lap_times):
    all_times = [time for times in lap_times.values() for time in times]
    return sum(all_times) / len(all_times)

# Function to plot fastest lap times as a pie chart
def plot_lap_times(lap_times):
    drivers = list(lap_times.keys())
    times = [min(times) for times in lap_times.values()]  # Fastest lap times
    total_time = sum(times)
    times_percentage = [time / total_time * 100 for time in times]  # Convert times to percentages

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(times_percentage, labels=drivers, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribution of Fastest Lap Times by Driver')
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    plt.show()

# Function to plot number of laps completed by drivers
def plot_laps_completed(lap_times):
    drivers = list(lap_times.keys())
    laps_completed = [len(times) for times in lap_times.values()]

    # Plotting the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(drivers, laps_completed, color='skyblue')
    plt.xlabel('Drivers')
    plt.ylabel('Number of Laps Completed')
    plt.title('Number of Laps Completed by Each Driver')
    plt.show()

# Function to rank drivers by lap times
def rank_drivers_by_time(lap_times):
    driver_rankings = []
    for driver, times in lap_times.items():
        fastest_time = min(times)
        avg_time = sum(times) / len(times)
        driver_rankings.append((driver, fastest_time, avg_time))
    
    # Sort by fastest lap time, descending order
    driver_rankings.sort(key=lambda x: x[1], reverse=True)  # Sort by fastest lap time
    return driver_rankings

# Function to compare two drivers
def compare_drivers(driver1, driver2, lap_times):
    driver1_times = lap_times.get(driver1, [])
    driver2_times = lap_times.get(driver2, [])
    
    if not driver1_times or not driver2_times:
        print(f"One or both drivers {driver1} or {driver2} have no lap times.\n")
        return
    
    driver1_best = min(driver1_times)
    driver2_best = min(driver2_times)
    
    print(f"Comparison between {driver1} and {driver2}:")
    print(f"{driver1} Best Lap: {driver1_best:.3f}")
    print(f"{driver2} Best Lap: {driver2_best:.3f}")
    print(f"Time Difference: {abs(driver1_best - driver2_best):.3f} seconds\n")

# Function to display a particular driver's details
def display_driver_details_with_lap_info(driver_code, driver_details, lap_times):
    driver_info = driver_details.get(driver_code)
    driver_lap_times = lap_times.get(driver_code)
    
    if not driver_info:
        print(f"Driver with code {driver_code} not found in details.\n")
        return

    if not driver_lap_times:
        print(f"Driver with code {driver_code} has no lap times recorded.\n")
        return

    fastest_time = min(driver_lap_times)
    average_time = sum(driver_lap_times) / len(driver_lap_times)

    print(f"Details for Driver {driver_code}:")
    print(f"ID: {driver_info['ID']}")
    print(f"Name: {driver_info['Name']}")
    print(f"Car: {driver_info['Car']}")
    print(f"Fastest Lap Time: {fastest_time:.3f}")
    print(f"Average Lap Time: {average_time:.3f}\n")


def main():
    filename = input("Enter the filename for lap times: ").strip()
    try:
        race_location, lap_times = load_driver_data(filename)
        display_race_location(race_location)

        # Find and display the fastest driver
        fastest_driver, fastest_time = find_fastest_driver(lap_times)
        print(f"Fastest Driver: {fastest_driver} with a time of {fastest_time:.3f} seconds\n")
        
        # Calculate and display average lap times
        overall_avg_time = calculate_overall_average_lap_time(lap_times)
        print(f"Overall Average Lap Time: {overall_avg_time:.3f} seconds\n")
        
        # Display driver ranking
        driver_rankings = rank_drivers_by_time(lap_times)
        print("Driver Rankings (Fastest Lap Time First):")
        print(tabulate(driver_rankings, headers=['Driver', 'Fastest Time', 'Average Time'], 
                       tablefmt='grid', floatfmt=".3f"))
        
        # Plot lap times as a pie chart
        show_chart = input("Do you want to see the chart of fastest lap times? (y/n): ").strip().lower()
        if show_chart == 'y':
            plot_lap_times(lap_times)

        show_bar = input("Do you want to see the graph of laps completed by drivers? (y/n): ").strip().lower()
        if show_bar == 'y':
            plot_laps_completed(lap_times)

          # Ask if the user wants to see driver details
        show_details = input("Do you want to see driver details? (y/n): ").strip().lower()
        if show_details == 'y':
            driver_details_file = input("Enter the filename for driver details: ").strip()
            driver_details = load_driver_details(driver_details_file)
            display_driver_details(driver_details)

            specific_driver = input("Do you want to see details for a specific driver? (y/n): ").strip().lower()
            if specific_driver == 'y':
                driver_code = input("Enter the driver code: ").strip()
                display_driver_details_with_lap_info(driver_code, driver_details, lap_times)

        # Ask if the user wants to compare two drivers
        compare = input("Do you want to compare two drivers? (y/n): ").strip().lower()
        if compare == 'y':
            driver1 = input("Enter first driver code: ").strip()
            driver2 = input("Enter second driver code: ").strip()
            compare_drivers(driver1, driver2, lap_times)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.\n")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

