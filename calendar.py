import subprocess
import dbus
import datetime
import re
import socket  # DODATO: Za kontrolu mrežnog vremena

# KLJUČ: Ako internet ne odgovori u roku od 10 sekundi, prekini sve
socket.setdefaulttimeout(10)

def get_goa_accounts():
    accounts = []
    try:
        bus = dbus.SessionBus()
        manager_obj = bus.get_object('org.gnome.OnlineAccounts', '/org/gnome/OnlineAccounts')
        manager = dbus.Interface(manager_obj, 'org.freedesktop.DBus.ObjectManager')
        # DODAT timeout za DBus upit
        objects = manager.GetManagedObjects(timeout=5)
        for path, interfaces in objects.items():
            if 'org.gnome.OnlineAccounts.Account' in interfaces:
                acc = interfaces['org.gnome.OnlineAccounts.Account']
                email = str(acc['PresentationIdentity'])
                if "gmail.com" in email:
                    accounts.append({'id': path.split('/')[-1], 'user': email})
    except: pass
    return accounts

def get_goa_token(acc_id):
    try:
        cmd = ["gdbus", "call", "--session", "--dest", "org.gnome.OnlineAccounts",
               "--object-path", f"/org/gnome/OnlineAccounts/Accounts/{acc_id}",
               "--method", "org.gnome.OnlineAccounts.OAuth2Based.GetAccessToken"]
        # DODAT timeout=5 za gdbus
        return subprocess.check_output(cmd, text=True, timeout=5).split("'")[1]
    except: return None

def fetch_via_caldav(user, token):
    url = f"https://apidata.googleusercontent.com/caldav/v2/{user}/events"
    now = datetime.datetime.now(datetime.timezone.utc)
    start_str = now.strftime("%Y%m%dT000000Z")
    end_str = (now + datetime.timedelta(days=7)).strftime("%Y%m%dT235959Z")

    xml_query = f"""
    <C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
      <D:prop><C:calendar-data /></D:prop>
      <C:filter>
        <C:comp-filter name="VCALENDAR">
          <C:comp-filter name="VEVENT">
            <C:time-range start="{start_str}" end="{end_str}"/>
          </C:comp-filter>
        </C:comp-filter>
      </C:filter>
    </C:calendar-query>
    """

    # DODAT --max-time 10 u curl komandu (ovo je ključno za kalendar)
    cmd = ["curl", "-s", "--max-time", "10", "-X", "REPORT", url, 
           "-H", f"Authorization: Bearer {token}",
           "-H", "Content-Type: application/xml", "--data", xml_query]

    try:
        # DODAT timeout=12 na nivou subprocess-a kao dupla zaštita
        response = subprocess.check_output(cmd, text=True, timeout=12)
        if not response or "<D:error" in response:
            # Ako primarni kalendar ne radi, probaj "primary" sa istim timeout-om
            cmd[4] = "https://apidata.googleusercontent.com/caldav/v2/primary/events"
            response = subprocess.check_output(cmd, text=True, timeout=12)

        titles = re.findall(r"SUMMARY:(.*)", response)
        starts = re.findall(r"DTSTART[:;](?:VALUE=DATE:)?(\d+T?\d*)", response)

        if not titles: return

        events = sorted(zip(starts, titles))
        meseci = ["", "Јануар", "Фебруар", "Март", "Април", "Мај", "Јун", "Јул", "Август", "Септембар", "Октобар", "Новембар", "Децембар"]
        
        seen = set()
        for start, title in events:
            clean_title = title.strip()
            if clean_title in seen: continue
            seen.add(clean_title)

            try:
                d = start[6:8]
                m_index = int(start[4:6])
                m = meseci[m_index]
                vreme = f"[{start[9:11]}:{start[11:13]}] " if "T" in start else ""
                print(f"{d}. {m}  —  {vreme}{clean_title}")
            except: continue
            
    except: pass

if __name__ == "__main__":
    nalozi = get_goa_accounts()
    for nalog in nalozi:
        token = get_goa_token(nalog['id'])
        if token:
            fetch_via_caldav(nalog['user'], token)
