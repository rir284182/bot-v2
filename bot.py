import sys
print("Python version:", sys.version)

try:
    import os
    print("1. os imported")
except Exception as e:
    print("ERROR importing os:", e)

try:
    from datetime import datetime
    print("2. datetime imported")
except Exception as e:
    print("ERROR importing datetime:", e)

try:
    from supabase import create_client, Client
    print("3. supabase imported")
except Exception as e:
    print("ERROR importing supabase:", e)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("4. telegram imported")
except Exception as e:
    print("ERROR importing telegram:", e)

print("5. Checking environment variables...")
for var in ["BOT_TOKEN", "SUPABASE_URL", "SUPABASE_KEY"]:
    val = os.getenv(var)
    if val:
        print(f"   {var} = {val[:15]}..." if len(val) > 15 else f"   {var} = {val}")
    else:
        print(f"   {var} NOT SET")

print("6. Script finished successfully.")
