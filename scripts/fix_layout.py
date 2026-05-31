"""
Fix 001-003: move history-detail-overlay outside sticky-toolbar, fix broken card layout.
"""
import re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the first section marker (after toolbar)
    section_mark = html.find('<!-- ======')
    if section_mark == -1:
        section_mark = html.find('<div class="section"')

    # Find overlay
    overlay_start = html.find('history-detail-overlay')
    if overlay_start == -1:
        print(f'{path}: no overlay found')
        return

    # Find the actual <div class="history-detail-overlay" tag start
    overlay_tag = html.rfind('<', overlay_start-200, overlay_start)
    if overlay_tag < 0:
        print(f'{path}: cant find overlay tag start')
        return

    # We need to find where overlay ends and extract it
    # Then place it right after the toolbar's sticky-toolbar closing div

    # Strategy: find the sticky-toolbar close, extract overlay block and place it after

    # Find sticky-toolbar open and close
    sticky_open = html.find('class="sticky-toolbar"')
    if sticky_open == -1:
        print(f'{path}: no sticky-toolbar')
        return

    # Find the </div> that closes sticky-toolbar - it's the one before section_mark
    # that isn't inside an overlay

    # Simpler: just remove the overlay block from inside toolbar
    # and insert it between toolbar close and first section

    # Find overlay's opening and matching close
    # Extract overlay block
    o_start = overlay_tag
    o_tag = html[overlay_tag:]

    # The overlay starts with <div class="history-detail-overlay"
    # We need to find its matching </div>
    # Count div nesting
    depth = 0
    o_end = o_start
    for i in range(o_start, len(html)):
        c = html[i]
        if c == '<':
            if html[i:i+4] == '<!--':
                comment_end = html.find('-->', i+4)
                if comment_end > -1:
                    i = comment_end + 3
                    continue
            if html[i:i+3] == '</d':
                depth -= 1
                if depth <= 0:
                    # This closing div finishes the overlay
                    o_end = html.find('>', i) + 1
                    break
                i = html.find('>', i)
            elif html[i:i+3] == '<di' and 'class="history-detail' not in html[i:i+100]:
                depth += 1
                i = html.find('>', i)
            elif html[i:i+3] == '</d' or html[i:i+2] == '<d':
                i = html.find('>', i)

    overlay_block = html[o_start:o_end]

    # Remove overlay from current position
    html = html[:o_start] + html[o_end:]

    # Now find where to insert it - after sticky-toolbar close
    # Find the close of sticky-toolbar
    st_end = section_mark
    # Actually let's insert it right before section_mark
    insert_pos = html.rfind('\n', 0, section_mark)
    if insert_pos < 0:
        insert_pos = section_mark

    html = html[:insert_pos] + '\n\n' + overlay_block + '\n\n' + html[insert_pos:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'{path}: fixed')

fix_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_001.html')
fix_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_002.html')
fix_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html')
print('Done')
