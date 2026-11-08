#!/usr/bin/env python3
"""
Sample 03: Parallel Processing - Collect Books from Multiple Years
Demo running multiple NovaAct instances in parallel
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel
from nova_act import NovaAct, ActError

class Book(BaseModel):
    title: str
    author: str

class BookList(BaseModel):
    books: list[Book]

def get_books(year: int) -> BookList | None:
    """
    Get NYT bestseller books by year
    """
    try:
        with NovaAct(
            starting_page=f"https://en.wikipedia.org/wiki/List_of_The_New_York_Times_number-one_books_of_{year}#Fiction",
            headless=True
        ) as nova:
            print(f"Worker processing year {year}...")
            
            result = nova.act(
                "Return the books in the Fiction list",
                schema=BookList.model_json_schema()
            )
            
            if not result.matches_schema:
                return None
            
            book_list = BookList.model_validate(result.parsed_response)
            print(f"Completed year {year}: {len(book_list.books)} books")
            return book_list
            
    except ActError as e:
        print(f"ActError for year {year}: {e}")
        return None
    except Exception as e:
        print(f"Error for year {year}: {e}")
        return None

def main():
    """Demo parallel processing with ThreadPoolExecutor"""
    
    # Check API key
    api_key = os.getenv('NOVA_ACT_API_KEY')
    if not api_key:
        print("Please set NOVA_ACT_API_KEY")
        return
    
    print("Sample 03: Parallel Processing")
    print("=" * 40)
    print("Running multiple NovaAct instances in parallel")
    
    # Years to collect
    years = [2020, 2021, 2022, 2023]
    all_books = []
    
    print(f"\nWill collect books from {len(years)} years: {years}")
    print("Using ThreadPoolExecutor with max_workers=3")
    
    # Set max workers = maximum browser sessions
    with ThreadPoolExecutor(max_workers=3) as executor:
        print("\nStarting parallel processing...")
        
        # Submit all tasks
        future_to_year = {
            executor.submit(get_books, year): year 
            for year in years
        }
        
        # Collect results
        for future in as_completed(future_to_year.keys()):
            year = future_to_year[future]
            try:
                book_list = future.result()
                if book_list is not None:
                    all_books.extend(book_list.books)
                    print(f"Added {len(book_list.books)} books from year {year}")
                else:
                    print(f"No data from year {year}")
            except Exception as e:
                print(f"Exception from year {year}: {e}")
    
    # Summary
    print(f"\nPARALLEL PROCESSING RESULTS:")
    print("=" * 40)
    print(f"Total books collected: {len(all_books)}")
    print(f"From {len(years)} years: {years}")
    
    if all_books:
        print(f"\nSample books:")
        for i, book in enumerate(all_books[:5], 1):
            print(f"   {i}. {book.title} - {book.author}")
        
        if len(all_books) > 5:
            print(f"   ... and {len(all_books) - 5} more books")
    
    print(f"\nThis example demonstrates:")
    print("   • ThreadPoolExecutor for parallel processing")
    print("   • Multiple NovaAct instances")
    print("   • Error handling with ActError")
    print("   • Browser use map-reduce pattern")

if __name__ == "__main__":
    main()
