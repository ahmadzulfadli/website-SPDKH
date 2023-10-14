from dbClass import *
# read---------------------------------------------------------

@app.route('/')
def index():
    # tampilkan data terakhir dalam format json
    lastDatas = Hutan.query.order_by(Hutan.timestamp.desc()).first()

    # Tampilkan 5 data terakhir dalam format json
    lastFiveDatas = Hutan.query.order_by(Hutan.timestamp.desc()).limit(5).all()

    # Tampilkan data 30 data terakhir dalam format json
    lastThirtyDatas = Hutan.query.order_by(Hutan.timestamp.desc()).limit(5).all()

    countData = Hutan.query.count()

    # Fluktuasi data sensor
    if countData > 0:
        lastTemperature = Hutan.query.order_by(Hutan.timestamp.desc()).first().temperature
        lastHumidity = Hutan.query.order_by(Hutan.timestamp.desc()).first().humidity
        lastMoisture = Hutan.query.order_by(Hutan.timestamp.desc()).first().moisture
        lastCo = Hutan.query.order_by(Hutan.timestamp.desc()).first().co
        lastRainfall = Hutan.query.order_by(Hutan.timestamp.desc()).first().rainfall

    fluktuasi = {
        "temperature": lastTemperature,
        "humidity": lastHumidity,
        "moisture": lastMoisture,
        "co": lastCo,
        "rainfall": lastRainfall
    }

    # Grafik data sensor
    grafikJson = []
    for item in lastThirtyDatas :
        grafikJson.append({
            'label': item.timestamp.strftime('%H:%M'),
            'temperature': item.temperature,
            'humidity': item.humidity,
            'moisture': item.moisture,
            'co': item.co,
            'rainfall': item.rainfall
        })
    
    return render_template('index.html', data = lastDatas, fluktuasi =fluktuasi, grafik = grafikJson, lastDatas = lastFiveDatas)


@app.route('/tabel')
def tabel():
    # tampilkan seluruh database
    hutanDatas = Hutan.query.all()

    return render_template('tabel.html', data = hutanDatas)

# link untuk input data
# localhost:5001/inputData?mode=save&temperature=30&humidity=79&moisture=50&co=0.5&count_tip=1

@app.route('/inputData', methods=['GET'])
def inputData():
    dateToday = date.today()
    HutanDataToday = Hutan.query.filter(Hutan.timestamp >= dateToday).filter(Hutan.timestamp < dateToday + timedelta(days=1)).all()
    countTipDataToday = sum([data.count_tip for data in HutanDataToday])

    try:
        mode = request.args.get('mode')
        if mode != 'save':
            return jsonify({"error": "Mode not found."}), 400

        else:
            temperature = request.args.get('temperature', type=float)
            humidity = request.args.get('humidity', type=float)
            moisture = request.args.get('moisture', type=float)
            co = request.args.get('co', type=float)
            count_tip = request.args.get('count_tip', type=int)

            print(temperature)

            if temperature is None or humidity is None or moisture is None or co is None or count_tip is None:
                return jsonify({"error": "Bad request."}), 400
            

            # count rainfall
            countTipDataAverageToday = countTipDataToday + count_tip

            if countTipDataAverageToday == 0:
                rainfall = 0
            
            rainfall = 0.33 * countTipDataAverageToday

            # algorithm for status
            status = "Aman" # aman

            if temperature > 37 and humidity < 50 and moisture < 15 and rainfall < 1:
                status = "Potensi kebakaran level 1" # potensi kebakaran level 1

            if temperature > 40 and humidity < 50 and moisture < 10 and rainfall < 1:
                status = "Potensi kebakaran level 2" # potensi kebakaran level 2

            if temperature > 43 and humidity < 50 and moisture < 5 and rainfall < 1:
                status = "Potensi kebakaran level 3" # potensi kebakaran level 3
            
            if co > 15:
                status = "Kebakaran" # kebakaran


            # upload data to database
            newSPDKHData = Hutan(
                temperature=temperature,
                humidity=humidity,
                moisture=moisture,
                co=co,
                count_tip=count_tip,
                rainfall=rainfall,
                status = status
            )

            db.session.add(newSPDKHData)

            db.session.commit()

            return redirect(url_for('lihatData'))

    except Exception as e:
        return jsonify({"error": "An error occurred while trying to add sensor data."}), 500


@app.route('/lihatData', methods=['GET'])
def lihatData():
    # tampilkan seluruh database dalam format json
    
    hutanDatas = Hutan.query.all()
    data = []
    for item in hutanDatas:
        data.append({
            "id": item.id,
            "temperature": item.temperature,
            "humidity": item.humidity,
            "moisture": item.moisture,
            "co": item.co,
            "rainfall": item.rainfall,
            "status": item.status,
            "timestamp": item.timestamp
        })

    response = {
        "status": "success",
        "message": "Sensor data added successfully!",
        "data": data
    }

    return jsonify(response), 200


if __name__ == '__main__':
    # Launch the application
    app.run(port = 5001, debug=True)
