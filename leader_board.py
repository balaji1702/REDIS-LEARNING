from redis_utility import RedisCacheManager
if __name__ == "__main__":
    manager = RedisCacheManager(password='TopSecretDevPass123!')
    
    if manager.ping_server():
        leaderboard = "games:high_scores"
        
        print("\n--- Phase 1: Submitting Live Player Scores ---")
        manager.update_score(leaderboard, "player_sam", 2750)
        manager.update_score(leaderboard, "player_alex", 4500)
        manager.update_score(leaderboard, "player_chris", 5100)
        
        # Simulating player_sam getting a massive power-up and updating their score!
        print("\n--- Phase 2: Player Sam gets a massive score update ---")
        manager.update_score(leaderboard, "player_sam", 6200)
        
        print("\n--- Phase 3: Fetching Live Top 3 Leaderboard ---")
        top_players = manager.get_top_rankings(leaderboard, top_n=3)
        
        for rank, (player, score) in enumerate(top_players, start=1):
            print(f"Rank {rank}: {player} with a score of {score}")