from flask import Flask, render_template, request, jsonify
from ipaddress import IPv4Network, summarize_address_range, IPv4Address

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form.get('option')
        
        if option == 'percentage_of_total':
            total_value = float(request.form.get('total_value'))
            percentage = float(request.form.get('percentage'))
            result = (percentage / 100) * total_value
            return jsonify({
                'result': result,
                'calculation': '전체값의 {}%는 {:.2f}'.format(percentage, result)
            })
        
        elif option == 'percentage_of_part':
            total_value = float(request.form.get('total_value'))
            part_value = float(request.form.get('part_value'))
            percentage = (part_value / total_value) * 100
            return jsonify({
                'result': percentage,
                'calculation': '전체값에서 {:.2f}은 {:.2f}%입니다.'.format(part_value, percentage)
            })
        
        elif option == 'percentage_change':
            old_value = float(request.form.get('old_value'))
            new_value = float(request.form.get('new_value'))
            percentage_change = ((new_value - old_value) / old_value) * 100
            if percentage_change > 0:
                change_type = '증가'
            else:
                change_type = '감소'
            return jsonify({
                'result': abs(percentage_change),
                'calculation': '값이 {:.2f}에서 {:.2f}로 {:.2f}% {}했습니다.'.format(old_value, new_value, abs(percentage_change), change_type)
            })
    
    return render_template('index.html')

@app.route('/cidr', methods=['GET', 'POST'])
def cidr():
    if request.method == 'POST':
        if 'cidr_input' in request.form:
            # CIDR to IP Range calculation
            try:
                cidr = request.form.get('cidr_input')
                network = IPv4Network(cidr)
                return jsonify({
                    'type': 'cidr_to_range',
                    'cidr_range': str(network),
                    'netmask': str(network.netmask),
                    'first_ip': str(network.network_address),
                    'last_ip': str(network.broadcast_address),
                    'total_hosts': network.num_addresses - 2  # Excluding network and broadcast addresses
                })
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
                
        elif 'start_ip' in request.form and 'end_ip' in request.form:
            # IP Range to CIDR calculation
            try:
                start_ip = IPv4Address(request.form.get('start_ip'))
                end_ip = IPv4Address(request.form.get('end_ip'))
                cidrs = list(summarize_address_range(start_ip, end_ip))
                return jsonify({
                    'type': 'range_to_cidr',
                    'cidrs': [str(cidr) for cidr in cidrs]
                })
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
                
    return render_template('cidr_cal.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
