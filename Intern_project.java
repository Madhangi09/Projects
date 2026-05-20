import java.util.*;

public class IPLTravelPlanner {

    static String[] teams = {
            "CSK", "MI", "RCB", "KKR", "DC",
            "SRH", "RR", "PBKS", "GT", "LSG"
    };

    static String[] grounds = {
            "Chennai", "Mumbai", "Bangalore", "Kolkata", "Delhi",
            "Hyderabad", "Jaipur", "Mohali", "Ahmedabad", "Lucknow"
    };

    // travel cost between cities
    static int[][] travel = {

            {0, 2000, 1500, 3000, 2500, 1800, 2200, 2700, 2400, 2600},
            {2000, 0, 1700, 2200, 1800, 2000, 2100, 1900, 2300, 2400},
            {1500, 1700, 0, 2500, 2000, 1200, 1600, 2100, 2200, 2300},
            {3000, 2200, 2500, 0, 1200, 2000, 1800, 1700, 2100, 2300},
            {2500, 1800, 2000, 1200, 0, 1500, 1400, 1600, 1700, 1300},
            {1800, 2000, 1200, 2000, 1500, 0, 1700, 1900, 2100, 2200},
            {2200, 2100, 1600, 1800, 1400, 1700, 0, 1300, 1500, 1600},
            {2700, 1900, 2100, 1700, 1600, 1900, 1300, 0, 1400, 1500},
            {2400, 2300, 2200, 2100, 1700, 2100, 1500, 1400, 0, 1200},
            {2600, 2400, 2300, 2300, 1300, 2200, 1600, 1500, 1200, 0}
    };

    public static void main(String[] args) {

        int leagueCost = 0;

        System.out.println("IPL 2026 Travel Schedule");
        System.out.println("-----------------------------------------");

        for (int i = 0; i < teams.length; i++) {

            boolean[] visited = new boolean[teams.length];

            int current = i;
            int teamCost = 0;

            visited[current] = true;

            System.out.println("\nTeam : " + teams[i]);
            System.out.println("Home Ground : " + grounds[i]);

            // away matches
            for (int match = 0; match < teams.length - 1; match++) {

                int next = -1;
                int min = Integer.MAX_VALUE;

                // finding nearest stadium
                for (int j = 0; j < teams.length; j++) {

                    if (!visited[j] && travel[current][j] < min) {

                        min = travel[current][j];
                        next = j;
                    }
                }

                visited[next] = true;

                System.out.println(
                        teams[i] + " vs " + teams[next]
                                + " at " + grounds[next]
                                + " -> Travel Cost : ₹" + min
                );

                teamCost += min;
                current = next;
            }

            // return back home
            int backHome = travel[current][i];

            System.out.println(
                    "Return to " + grounds[i]
                            + " -> Cost : ₹" + backHome
            );

            teamCost += backHome;

            System.out.println("Total Cost for " + teams[i]
                    + " : ₹" + teamCost);

            System.out.println("-----------------------------------------");

            leagueCost += teamCost;
        }

        System.out.println("\nOverall IPL Travel Expense : ₹" + leagueCost);
    }
}