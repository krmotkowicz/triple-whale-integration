
import json
import sqlite3
from pathlib import Path

DATA_FILE = Path("files/orders_bulk.json")
DB_FILE = Path("orders.db")


def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                created_at TEXT,
                currency TEXT,
                order_revenue REAL
            )
        """)

        with DATA_FILE.open(encoding="utf-8") as f:
            data = json.load(f)

        orders = data if isinstance(data, list) else data.get("orders", [])

        for order in orders:
            conn.execute("""
                INSERT OR REPLACE INTO orders
                (order_id, created_at, currency, order_revenue)
                VALUES (?, ?, ?, ?)
            """, (
                str(order["order_id"]),
                order.get("created_at"),
                order.get("currency"),
                order.get("order_revenue")
            ))

    print(f"Local database ready: {DB_FILE}")


def check_order(order_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row

        result = conn.execute("""
            SELECT order_id, created_at, currency, order_revenue
            FROM orders
            WHERE order_id = ?
        """, (order_id,)).fetchone()

    print("\n--- LOCAL SQL ORDER CHECK ---")

    if result:
        print("Status: FOUND")
        print("Order ID:", result["order_id"])
        print("Created:", result["created_at"])
        print("Revenue:", result["order_revenue"])
        print("Currency:", result["currency"])
    else:
        print("Status: NOT FOUND")

    print("Source: Local SQLite DB check")
   ## print("Triple Whale status: NOT CHECKED") - in the future 


if __name__ == "__main__":
    initialize_database()

    while True:
        order_id = input("\nEnter Order ID (or q to quit): ").strip()

        if order_id.lower() == "q":
            break

        if order_id:
            check_order(order_id)
