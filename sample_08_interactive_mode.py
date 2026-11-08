#!/usr/bin/env python3
"""
Sample 08: Interactive Mode Demo
Demo sử dụng Nova Act trong interactive mode
"""

import os
import sys
from nova_act import NovaAct

def demo_interactive_session():
    """Demo interactive session với user input"""
    
    print("Demo Interactive Session")
    print("-" * 30)
    print("Bạn có thể nhập commands để điều khiển Nova Act")
    print("Gõ 'quit' để thoát")
    
    try:
        # Khởi tạo Nova Act
        nova = NovaAct(starting_page="https://www.amazon.com")
        nova.start()
        
        print("Nova Act đã khởi động!")
        print("Đã mở Amazon.com")
        
        while True:
            print("\n" + "="*40)
            print("Interactive Mode")
            print("="*40)
            
            # Hiển thị menu
            print("Commands có sẵn:")
            print("   1. search <product> - Tìm kiếm sản phẩm")
            print("   2. click <element> - Click vào element")
            print("   3. scroll <direction> - Scroll trang")
            print("   4. goto <url> - Đi đến URL")
            print("   5. screenshot - Chụp màn hình")
            print("   6. custom - Nhập command tùy chỉnh")
            print("   7. quit - Thoát")
            
            # Lấy input từ user
            choice = input("\nChọn command (1-7): ").strip()
            
            if choice == "1":
                product = input("Nhập tên sản phẩm: ")
                print(f"Đang tìm kiếm: {product}")
                result = nova.act(f"search for {product}")
                print(f"Kết quả: {result.response}")
                
            elif choice == "2":
                element = input("Nhập element cần click: ")
                print(f"Đang click: {element}")
                result = nova.act(f"click on {element}")
                print(f"Kết quả: {result.response}")
                
            elif choice == "3":
                direction = input("Nhập hướng scroll (up/down): ")
                print(f"Đang scroll {direction}")
                result = nova.act(f"scroll {direction}")
                print(f"Kết quả: {result.response}")
                
            elif choice == "4":
                url = input("Nhập URL: ")
                print(f"Đang đi đến: {url}")
                nova.go_to_url(url)
                print("Đã chuyển trang")
                
            elif choice == "5":
                print("Đang chụp screenshot...")
                screenshot = nova.page.screenshot()
                with open("interactive_screenshot.png", "wb") as f:
                    f.write(screenshot)
                print("Đã lưu screenshot: interactive_screenshot.png")
                
            elif choice == "6":
                custom_command = input("Nhập command tùy chỉnh: ")
                print(f"Đang thực hiện: {custom_command}")
                result = nova.act(custom_command)
                print(f"Kết quả: {result.response}")
                
            elif choice == "7" or choice.lower() == "quit":
                print("Đang thoát interactive mode...")
                break
                
            else:
                print("Command không hợp lệ")
            
            # Hỏi có muốn tiếp tục
            continue_choice = input("\nTiếp tục? (y/N): ")
            if continue_choice.lower() != 'y':
                break
        
        # Dọn dẹp
        nova.stop()
        print("Đã đóng Nova Act session")
        
    except KeyboardInterrupt:
        print("\nInteractive session bị dừng")
    except Exception as e:
        print(f"Lỗi: {e}")

def demo_step_by_step_workflow():
    """Demo workflow từng bước với user confirmation"""
    
    print("\nDemo Step-by-Step Workflow")
    print("-" * 30)
    
    try:
        nova = NovaAct(starting_page="https://www.amazon.com")
        nova.start()
        
        # Workflow: Tìm và thêm sản phẩm vào cart
        steps = [
            ("Tìm kiếm coffee maker", "search for coffee maker"),
            ("Chọn sản phẩm đầu tiên", "click on the first product"),
            ("Thêm vào giỏ hàng", "add to cart"),
            ("Đi đến giỏ hàng", "go to cart")
        ]
        
        print(f"Workflow có {len(steps)} bước:")
        for i, (desc, _) in enumerate(steps, 1):
            print(f"   {i}. {desc}")
        
        for i, (description, command) in enumerate(steps, 1):
            print(f"\n{'='*40}")
            print(f"Bước {i}/{len(steps)}: {description}")
            print(f"{'='*40}")
            
            # Hỏi user có muốn thực hiện bước này
            proceed = input(f"Thực hiện bước này? (Y/n): ")
            if proceed.lower() == 'n':
                print("Bỏ qua bước này")
                continue
            
            print(f"Đang thực hiện: {command}")
            try:
                result = nova.act(command)
                print(f"Hoàn thành: {result.response}")
            except Exception as e:
                print(f"Lỗi bước {i}: {e}")
                
                # Hỏi có muốn tiếp tục
                continue_choice = input("Tiếp tục workflow? (y/N): ")
                if continue_choice.lower() != 'y':
                    break
            
            # Pause giữa các bước
            input("Nhấn Enter để tiếp tục bước tiếp theo...")
        
        nova.stop()
        print("Workflow hoàn thành!")
        
    except Exception as e:
        print(f"Lỗi workflow: {e}")

def demo_debugging_session():
    """Demo debugging với breakpoints"""
    
    print("\nDemo Debugging Session")
    print("-" * 30)
    
    try:
        nova = NovaAct(
            starting_page="https://example.com",
            headless=False  # Cần thấy để debug
        )
        nova.start()
        
        print("Debugging mode - có thể inspect từng bước")
        
        # Breakpoint 1
        print("\nBreakpoint 1: Kiểm tra trang đã load")
        input("Debug: Kiểm tra trang web, nhấn Enter để tiếp tục...")
        
        result = nova.act("get the main heading of the page")
        print(f"Heading: {result.response}")
        
        # Breakpoint 2
        print("\nBreakpoint 2: Sau khi lấy heading")
        print("Debug options:")
        print("   1. Chụp screenshot")
        print("   2. Lấy page content")
        print("   3. Kiểm tra URL hiện tại")
        print("   4. Tiếp tục")
        
        debug_choice = input("Chọn debug action (1-4): ")
        
        if debug_choice == "1":
            screenshot = nova.page.screenshot()
            with open("debug_screenshot.png", "wb") as f:
                f.write(screenshot)
            print("Đã lưu debug screenshot")
            
        elif debug_choice == "2":
            content = nova.page.content()
            print(f"Page content length: {len(content)} chars")
            
        elif debug_choice == "3":
            current_url = nova.page.url
            print(f"Current URL: {current_url}")
        
        # Breakpoint 3
        print("\nBreakpoint 3: Thực hiện action cuối")
        input("Debug: Nhấn Enter để scroll trang...")
        
        nova.act("scroll down to see more content")
        
        # Final debug
        print("\nFinal Debug: Session summary")
        print("Debug info:")
        print(f"   Page title: {nova.page.title()}")
        print(f"   Final URL: {nova.page.url}")
        
        nova.stop()
        print("Debug session hoàn thành!")
        
    except Exception as e:
        print(f"Lỗi debug: {e}")

def main():
    """Demo interactive mode"""
    
    # Kiểm tra API key
    api_key = os.getenv('NOVA_ACT_API_KEY')
    if not api_key:
        print("Vui lòng set NOVA_ACT_API_KEY")
        return
    
    print("Sample 08: Interactive Mode Demo")
    print("=" * 50)
    print("Demo sử dụng Nova Act interactively")
    
    print("\nInteractive Mode Features:")
    print("   • Manual control của Nova Act")
    print("   • Step-by-step workflow")
    print("   • Debugging với breakpoints")
    print("   • User input và confirmation")
    print("   • Real-time interaction")
    
    # Menu chọn demo
    demos = [
        ("Interactive Session", demo_interactive_session),
        ("Step-by-Step Workflow", demo_step_by_step_workflow),
        ("Debugging Session", demo_debugging_session)
    ]
    
    print(f"\nChọn demo để chạy:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"   {i}. {name}")
    print(f"   4. Chạy tất cả")
    
    choice = input("\nChọn demo (1-4): ").strip()
    
    if choice in ["1", "2", "3"]:
        demo_index = int(choice) - 1
        demo_name, demo_func = demos[demo_index]
        
        print(f"\nChạy {demo_name}")
        try:
            demo_func()
        except Exception as e:
            print(f"Lỗi: {e}")
            
    elif choice == "4":
        print("\nChạy tất cả demo")
        for demo_name, demo_func in demos:
            print(f"\n{'='*50}")
            print(f"{demo_name}")
            print(f"{'='*50}")
            
            try:
                demo_func()
            except KeyboardInterrupt:
                print("Demo bị dừng")
                break
            except Exception as e:
                print(f"Lỗi: {e}")
    else:
        print("Lựa chọn không hợp lệ")
    
    print(f"\nInteractive Mode Tips:")
    print("   • Sử dụng nova.start() và nova.stop() để control session")
    print("   • Có thể manipulate browser giữa các act() calls")
    print("   • Ctrl+X để exit action, Ctrl+C để exit browser")
    print("   • Sử dụng input() để tạo breakpoints")
    print("   • nova.page để access Playwright Page object")

if __name__ == "__main__":
    main()
