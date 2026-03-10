import sqlite3
import os
import sys
import glob
import socket

# SAFETY: Maximum script execution time (Zombie Protection)
socket.setdefaulttimeout(5)

def get_db_path():
    # Search for any cache.db within the Evolution addressbook directory
    pattern = os.path.expanduser("~/.cache/evolution/addressbook/*/cache.db")
    found_files = glob.glob(pattern)
    
    if not found_files:
        return None
    
    # Sort by modification time to always pick the most recent database
    found_files.sort(key=os.path.getmtime, reverse=True)
    return found_files[0]

def search_contacts(term=""):
    db_path = get_db_path()
    
    if not db_path or not os.path.exists(db_path):
        print("ERROR | Database not found!")
        return

    conn = None
    try:
        # Connect in Read-Only (ro) and No-Lock mode to prevent system hang
        conn = sqlite3.connect(f"file:{db_path}?mode=ro&nolock=1", uri=True)
        cursor = conn.cursor()
        
        # ENHANCED QUERY: Search by Name OR Phone Number (Reverse Lookup)
        query = """
            SELECT full_name, ECacheOBJ 
            FROM ECacheObjects 
            WHERE full_name LIKE ? OR ECacheOBJ LIKE ?
            ORDER BY full_name ASC 
            LIMIT 30
        """
        search_param = f'%{term}%'
        cursor.execute(query, (search_param, search_param))
        
        results = cursor.fetchall()
        if not results:
            print("INFO | No results found for this term.")
            return

        for name, vcard in results:
            phone = "/"
            if vcard:
                # Extract phone number from vCard data
                vcard_str = str(vcard)
                lines = vcard_str.splitlines()
                for line in lines:
                    if "TEL" in line and ":" in line:
                        phone = line.split(":")[-1].replace(";", " ").strip()
                        break
            
            # Print in clear format for XFCE Genmon or Terminal
            print(f"{str(name).upper()} | {phone}")

    except Exception as e:
        print(f"ERROR | {str(e)}")
    finally:
        # Always close connection to prevent file handles leak
        if conn:
            conn.close()

if __name__ == "__main__":
    # If run without arguments, it will list all contacts (up to the limit)
    search_term = sys.argv[1] if len(sys.argv) > 1 else ""
    search_contacts(search_term)
