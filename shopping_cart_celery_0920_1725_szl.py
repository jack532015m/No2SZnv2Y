# 代码生成时间: 2025-09-20 17:25:45
from celery import Celery
import json
from flask import Flask, request, jsonify

# 初始化Celery
app = Flask(__name__)
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
celery = Celery(__name__, broker=broker_url, backend=result_backend)

# 定义购物车数据结构，这里简单使用字典模拟
cart = {}

# 添加商品到购物车
@celery.task(bind=True)
def add_product_to_cart(self, cart_id, product_id, quantity):
    try:
        if cart_id not in cart:
            cart[cart_id] = {}
        cart[cart_id][product_id] = quantity
        return jsonify({'message': 'Product added to cart', 'cart_id': cart_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取购物车内容
@app.route('/get_cart/<cart_id>', methods=['GET'])
def get_cart(cart_id):
    try:
        cart_items = cart.get(cart_id, {})
        return jsonify(cart_items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新购物车中的商品数量
@celery.task(bind=True)
def update_product_in_cart(self, cart_id, product_id, quantity):
    try:
        if cart_id in cart and product_id in cart[cart_id]:
            cart[cart_id][product_id] = quantity
            return jsonify({'message': 'Product quantity updated', 'cart_id': cart_id}), 200
        else:
            return jsonify({'error': 'Product not found in cart'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除购物车中的商品
@celery.task(bind=True)
def remove_product_from_cart(self, cart_id, product_id):
    try:
        if cart_id in cart and product_id in cart[cart_id]:
            del cart[cart_id][product_id]
            return jsonify({'message': 'Product removed from cart', 'cart_id': cart_id}), 200
        else:
            return jsonify({'error': 'Product not found in cart'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 清空购物车
@celery.task(bind=True)
def clear_cart(self, cart_id):
    try:
        if cart_id in cart:
            del cart[cart_id]
            return jsonify({'message': 'Cart cleared', 'cart_id': cart_id}), 200
        else:
            return jsonify({'error': 'Cart not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)