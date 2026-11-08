#!/usr/bin/env python3
"""
Sample 04: Authentication and Persistent Browser State
Demo using user_data_dir to store sessions
"""

import os
import tempfile
from nova_act import NovaAct, BOOL_SCHEMA

def setup_authenticated_session():
    """Setup session with authentication"""
    
    # Create user data directory
    user_data_dir = tempfile.mkdtemp(prefix="nova_act_session_")
    print(f"Created user data directory: {user_data_dir}")
    
    try:
        with NovaAct(
            starting_page="https://amazon.com/",
            user_data_dir=user_data_dir,
            clone_user_data_dir=False,  # Don't clone to preserve session
            headless=False  # Need GUI for user login
        ) as nova:
            
            print("Please log into the required websites...")
            print("Press Enter after you have finished logging in...")
            input()
            
            # Check login status
            result = nova.act("Am I logged in?", schema=BOOL_SCHEMA)
            
            if result.matches_schema:
                if result.parsed_response:
                    print("Successfully logged in!")
                else:
                    print("Not logged in")
            else:
                print("Cannot determine login status")
        
        print(f"Session saved at: {user_data_dir}")
        return user_data_dir
        
    except Exception as e:
        print(f"Error setting up session: {e}")
        return None

def use_authenticated_session(user_data_dir: str):
    """Use authenticated session"""
    
    if not user_data_dir or not os.path.exists(user_data_dir):
        print("User data directory does not exist")
        return
    
    try:
        with NovaAct(
            starting_page="https://amazon.com/",
            user_data_dir=user_data_dir,
            clone_user_data_dir=False,  # Use existing session
            headless=True
        ) as nova:
            
            print("Checking login status...")
            result = nova.act("Am I logged in?", schema=BOOL_SCHEMA)
            
            if result.matches_schema and result.parsed_response:
                print("Still logged in!")
                
                # Perform actions that require authentication
                print("Checking cart...")
                nova.act("go to my cart")
                
                print("Checking order history...")
                nova.act("go to my orders")
                
            else:
                print("Session expired, need to log in again")
                
    except Exception as e:
        print(f"Error using session: {e}")

def demo_parallel_with_cloning(user_data_dir: str):
    """Demo parallel processing with session cloning"""
    
    if not user_data_dir:
        return
    
    print("\nDemo Parallel Processing with Session Cloning")
    print("-" * 50)
    
    from concurrent.futures import ThreadPoolExecutor
    
    def worker_task(worker_id: int):
        """Task for each worker"""
        try:
            with NovaAct(
                starting_page="https://amazon.com/",
                user_data_dir=user_data_dir,
                clone_user_data_dir=True,  # Clone for parallel processing
                headless=True
            ) as nova:
                print(f"Worker {worker_id} checking login...")
                result = nova.act("Am I logged in?", schema=BOOL_SCHEMA)
                
                if result.matches_schema and result.parsed_response:
                    print(f"Worker {worker_id}: Logged in")
                    return f"Worker {worker_id}: Success"
                else:
                    print(f"Worker {worker_id}: Not logged in")
                    return f"Worker {worker_id}: Failed"
                    
        except Exception as e:
            print(f"Worker {worker_id} error: {e}")
            return f"Worker {worker_id}: Error"
    
    # Run 3 workers in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker_task, i) for i in range(1, 4)]
        results = [future.result() for future in futures]
    
    print("Parallel processing results:")
    for result in results:
        print(f"   • {result}")

def main():
    """Demo authentication and persistent sessions"""
    
    # Check API key
    api_key = os.getenv('NOVA_ACT_API_KEY')
    if not api_key:
        print("Please set NOVA_ACT_API_KEY")
        return
    
    print("Sample 04: Authentication & Persistent Sessions")
    print("=" * 50)
    print("Demo user_data_dir and session management")
    
    print("\nSteps:")
    print("1. Setup authenticated session")
    print("2. Use authenticated session")
    print("3. Demo parallel processing with cloning")
    
    # Step 1: Setup session
    print(f"\nSTEP 1: Setup Authenticated Session")
    print("-" * 30)
    user_data_dir = setup_authenticated_session()
    
    if not user_data_dir:
        print("Cannot setup session")
        return
    
    # Step 2: Use session
    print(f"\nSTEP 2: Use Authenticated Session")
    print("-" * 30)
    use_authenticated_session(user_data_dir)
    
    # Step 3: Parallel processing
    demo_parallel_with_cloning(user_data_dir)
    
    print(f"\nThis example demonstrates:")
    print("   • user_data_dir for persistent sessions")
    print("   • clone_user_data_dir=False to preserve session")
    print("   • clone_user_data_dir=True for parallel processing")
    print("   • BOOL_SCHEMA for yes/no responses")
    print("   • Authentication state management")
    
    print(f"\nSession data saved at: {user_data_dir}")
    print("You can delete this directory after testing")

if __name__ == "__main__":
    main()
