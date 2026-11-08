#!/usr/bin/env python3
"""
Sample 01: Order Coffee Maker on Amazon
Basic demo following Quick Start from official README
"""

import os
from nova_act import NovaAct

def main():
    """Demo ordering coffee maker - following Quick Start guide"""
    
    # Check API key
    api_key = os.getenv('NOVA_ACT_API_KEY')
    if not api_key:
        print("Please set NOVA_ACT_API_KEY")
        print("export NOVA_ACT_API_KEY='your_api_key_here'")
        return
    
    print("Sample 01: Order Coffee Maker")
    print("=" * 40)
    print("Following Quick Start from official README")
    
    try:
        # Script mode - following README
        with NovaAct(starting_page="https://www.amazon.com") as nova:
            print("Searching for coffee maker...")
            nova.act("search for a coffee maker")
            
            print("Selecting first product...")
            nova.act("select the first result")
            
            print("Adding to cart...")
            nova.act("scroll down or up until you see 'add to cart' and then click 'add to cart'")
            
            print("Successfully added coffee maker to cart!")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Try running with headless=False to see browser directly")

if __name__ == "__main__":
    main()
