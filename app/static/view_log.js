function updateCharts(callDict) {
    if (callDict['change']=='true') {
        if ('mdata' in callDict) {
            monthChart['data']['datasets'][0]['data'] = callDict['mdata'];
            monthChart.update();
            mdata = callDict['mdata']
        }
        if ('wdata' in callDict) {
            weekChart['data']['datasets'][0]['data'] = callDict['wdata'];
            weekChart.update();
            wdata = callDict['wdata']
        };
    };
};

function updateTables(returnDict) {
    var monthtable = document.getElementById('monthBody');
    var weektable = document.getElementById('weekBody');
    if (returnDict['change']=='true') {
        if ('monthlog' in returnDict) {
            var length = returnDict['monthlog'].length
            for (var i=0;i<length;i++) {
                var template = '<tr> \
                    <td id="firstTemp"></td> \
                    <td id="secondTemp"></td> \
                    <td id="thirdTemp"></td> \
                    <td id="fourthTemp"></td> \
                    <td id="fifthTemp"></td> \
                </tr>';
                monthtable.innerHTML += template;
                document.getElementById('firstTemp').innerText = returnDict['monthlog'][i]['level'];
                document.getElementById('firstTemp').removeAttribute('id');
                document.getElementById('secondTemp').innerText = returnDict['monthlog'][i]['datetime'];
                document.getElementById('secondTemp').removeAttribute('id');
                document.getElementById('thirdTemp').innerText = returnDict['monthlog'][i]['event'];
                document.getElementById('thirdTemp').removeAttribute('id');
                document.getElementById('fourthTemp').innerText = returnDict['monthlog'][i]['address'];
                document.getElementById('fourthTemp').removeAttribute('id');
                var fifth = document.getElementById('fifthTemp');
                if ('email' in returnDict['monthlog'][i]) {
                    var temp = '';
                    temp = temp.concat('email: ', returnDict['monthlog'][i]['email'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('email_entered' in returnDict['monthlog'][i]) {
                    var temp = '';
                    temp = temp.concat('entered email: ', returnDict['monthlog'][i]['email_entered'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('entered_pass' in returnDict['monthlog'][i]) {
                    var temp = '';
                    temp = temp.concat('entered password: ', returnDict['monthlog'][i]['entered_pass'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('unknown' in returnDict['monthlog'][i]) {
                    fifth.innerHTML += returnDict['monthlog'][i]['unknown'];
                };
                fifth.removeAttribute('id');
                monthlog.push(returnDict['monthlog'][i])
            };
        };
        if ('weeklog' in returnDict) {
            var length = returnDict['weeklog'].length
            for (var i=0;i<length;i++) {
                var template = '<tr> \
                    <td id="firstTemp"></td> \
                    <td id="secondTemp"></td> \
                    <td id="thirdTemp"></td> \
                    <td id="fourthTemp"></td> \
                    <td id="fifthTemp"></td> \
                </tr>';
                weektable.innerHTML += template;
                document.getElementById('firstTemp').innerText = returnDict['weeklog'][i]['level'];
                document.getElementById('firstTemp').removeAttribute('id');
                document.getElementById('secondTemp').innerText = returnDict['weeklog'][i]['datetime'];
                document.getElementById('secondTemp').removeAttribute('id');
                document.getElementById('thirdTemp').innerText = returnDict['weeklog'][i]['event'];
                document.getElementById('thirdTemp').removeAttribute('id');
                document.getElementById('fourthTemp').innerText = returnDict['weeklog'][i]['address'];
                document.getElementById('fourthTemp').removeAttribute('id');
                var fifth = document.getElementById('fifthTemp');
                if ('email' in returnDict['weeklog'][i]) {
                    var temp = '';
                    temp = temp.concat('email: ', returnDict['weeklog'][i]['email'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('email_entered' in returnDict['weeklog'][i]) {
                    var temp = '';
                    temp = temp.concat('entered email: ', returnDict['weeklog'][i]['email_entered'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('entered_pass' in returnDict['weeklog'][i]) {
                    var temp = '';
                    temp = temp.concat('entered password: ', returnDict['weeklog'][i]['entered_pass'], '<br>');
                    fifth.innerHTML += temp;
                };
                if ('unknown' in returnDict['weeklog'][i]) {
                    fifth.innerHTML += returnDict['weeklog'][i]['unknown'];
                };
                fifth.removeAttribute('id');
                weeklog.push(returnDict['weeklog'][i])
            };
        };
    };
};

function past8LevelChange(level) {
    if (level=='debug') {
        past8Chart['data']['datasets'][0]['label'] = 'Debug';
        past8Chart['data']['datasets'][0]['data'] = past8data[0];
        past8Chart['data']['datasets'][0]['borderColor'] = 'rgb(169,169,169)';
        past8Chart.update();
    }
    else if (level=='info') {
        past8Chart['data']['datasets'][0]['label'] = 'Info';
        past8Chart['data']['datasets'][0]['data'] = past8data[1];
        past8Chart['data']['datasets'][0]['borderColor'] = 'rgb(173,255,47)';
        past8Chart.update();
    }
    else if (level=='warning') {
        past8Chart['data']['datasets'][0]['label'] = 'Warning';
        past8Chart['data']['datasets'][0]['data'] = past8data[2];
        past8Chart['data']['datasets'][0]['borderColor'] = 'rgb(255,255,0)';
        past8Chart.update();
    }
    else if (level=='error') {
        past8Chart['data']['datasets'][0]['label'] = 'Error';
        past8Chart['data']['datasets'][0]['data'] = past8data[3];
        past8Chart['data']['datasets'][0]['borderColor'] = 'rgb(255,99,71)';
        past8Chart.update();
    }
    else if (level=='critical') {
        past8Chart['data']['datasets'][0]['label'] = 'Critical';
        past8Chart['data']['datasets'][0]['data'] = past8data[4];
        past8Chart['data']['datasets'][0]['borderColor'] = 'rgb(255,0,0)';
        past8Chart.update();
    }
};

function updatePast8Charts(returnDict) {
    if ('data' in returnDict) {
        past8data = returnDict['data'];
        var level = document.getElementById('past8LevelCheck').value;
        if (level=='debug') {
            past8Chart['data']['datasets'][0]['data'] = past8data[0];
            past8Chart.update();
        }
        else if (level=='info') {
            past8Chart['data']['datasets'][0]['data'] = past8data[1];
            past8Chart.update();
        }
        else if (level=='warning') {
            past8Chart['data']['datasets'][0]['data'] = past8data[2];
            past8Chart.update();
        }
        else if (level=='error') {
            past8Chart['data']['datasets'][0]['data'] = past8data[3];
            past8Chart.update();
        }
        else if (level=='critical') {
            past8Chart['data']['datasets'][0]['data'] = past8data[4];
            past8Chart.update();
        }
    }
};

function updatePast8Tables(returnDict) {
    var table = document.getElementById('past8Body');
    if (returnDict['change']=='true') {
        var length = returnDict[8].length
        for (var i=0;i<length;i++) {
            var template = '<tr> \
                <td id="firstTemp"></td> \
                <td id="secondTemp"></td> \
                <td id="thirdTemp"></td> \
                <td id="fourthTemp"></td> \
                <td id="fifthTemp"></td> \
            </tr>';
            table.innerHTML += template;
            document.getElementById('firstTemp').innerText = returnDict[8][i]['level'];
            document.getElementById('firstTemp').removeAttribute('id');
            document.getElementById('secondTemp').innerText = returnDict[8][i]['datetime'];
            document.getElementById('secondTemp').removeAttribute('id');
            document.getElementById('thirdTemp').innerText = returnDict[8][i]['event'];
            document.getElementById('thirdTemp').removeAttribute('id');
            document.getElementById('fourthTemp').innerText = returnDict[8][i]['address'];
            document.getElementById('fourthTemp').removeAttribute('id');
            var fifth = document.getElementById('fifthTemp');
            if ('email' in returnDict[8][i]) {
                var temp = '';
                temp = temp.concat('email: ', returnDict[8][i]['email'], '<br>');
                fifth.innerHTML += temp;
            };
            if ('email_entered' in returnDict[8][i]) {
                var temp = '';
                temp = temp.concat('entered email: ', returnDict[8][i]['email_entered'], '<br>');
                fifth.innerHTML += temp;
            };
            if ('entered_pass' in returnDict[8][i]) {
                var temp = '';
                temp = temp.concat('entered password: ', returnDict[8][i]['entered_pass'], '<br>');
                fifth.innerHTML += temp;
            };
            if ('unknown' in returnDict[8][i]) {
                fifth.innerHTML += returnDict[8][i]['unknown'];
            };
            fifth.removeAttribute('id');
            past8log[7].push(returnDict[8][i])
        };
    }
};


function updatePassMonitor(returnDict) {
    table = document.getElementById('pmBody');
    data = returnDict['data'];
    if ('changed' in returnDict) {
        var length = returnDict['length']
        console.log(data)
        table.innerHTML = "";
        console.log('cleared')
        console.log(length)
        for (var i=0;i<length;i++) {
            console.log(i)
            var template = '<tr id="temprow"> \
                <td id="firstTemp"></td> \
                <td id="secondTemp"></td> \
                <td id="thirdTemp"></td> \
                <td id="fourthTemp"></td> \
            </tr>';
            table.innerHTML += template;
            console.log('add row')
            if (data[i]['attempts'] > 4 && data[i]['attempts'] <9) {
                console.log(data[i]['attempts'], 'warn')
                document.getElementById('temprow').classList.add('table-warning');
            }
            else if (data[i]['attempts'] > 8) {
                console.log(data[i]['attempts'], 'danger')
                document.getElementById('temprow').classList.add('table-danger');
            };
            document.getElementById('temprow').removeAttribute('id');
            document.getElementById('firstTemp').innerText = data[i]['account_type'];
            document.getElementById('secondTemp').innerText = data[i]['email'];
            document.getElementById('thirdTemp').innerText = data[i]['attempts'];
            console.log('added one to three')
            var modal = "<div class='text-center'> \
                <button id='tempBtn' type='button' class='btn btn-secondary' data-bs-toggle='modal' style='background-color:#6c757d'>Review</button> \
            </div> \
            <div class='modal fade' id='tempModal' data-bs-backdrop='static' data-bs-keyboard='false' tabindex='-1' aria-hidden='true'> \
                <div class='modal-dialog modal-xl'> \
                    <div class='modal-content'> \
                        <div class='modal-header'> \
                            <h5 class='modal-title h5' id='tempTitle'></h5> \
                            <button type='button' class='btn-close overlap' data-bs-dismiss='modal' aria-label='Close'></button> \
                        </div> \
                        <div class='modal-body'> \
                            <br> \
                            <div class='row'> \
                                <!--insert filters--> \
                                <div style='height:400px;overflow-y:auto'> \
                                    <table class='table table-hover'> \
                                        <thead style='position:sticky;top:0;z-index:1;background:#eee'> \
                                            <tr> \
                                                <th>Date and Time</th> \
                                                <th>IP</th> \
                                                <th>Entered Password</th> \
                                            </tr> \
                                        </thead> \
                                        <tbody id='tempTable'> \
                                        </tbody> \
                                    </table> \
                                </div> \
                            </div> \
                        </div> \
                        <div class='modal-footer'> \
                            <button type='button' class='btn btn-secondary' data-bs-dismiss='modal' style='background-color:#6c757d'>Close</button> \
                        </div> \
                    </div> \
                </div> \
            </div>";
            document.getElementById('fourthTemp').innerHTML = modal;
            var target = ''
            target = target.concat('#passMonitor', i.toString(), 'Modal');
            document.getElementById('tempBtn').setAttribute('data-bs-target', target);
            var temp = ''
            temp = temp.concat('passMonitor', i.toString(), 'Modal');
            var tempModal = document.getElementById('tempModal');
            tempModal.setAttribute('id', temp);
            temp = ''
            temp = temp.concat('passMonitor', i.toString(), 'Label');
            tempModal.setAttribute('aria-labelledby', temp);
            var tempTitle = document.getElementById('tempTitle');
            tempTitle.setAttribute('id', temp);
            temp = ''
            tempTitle.innerText = temp.concat('Attack ', (i+1).toString());
            var attacks = data[i]['data'];
            for (var x=0;x<data[i]['attempts'];x++) {
                var modalTemplate = "<tr> \
                    <td id='modalFirst'></td> \
                    <td id='modalSecond'></td> \
                    <td id='modalThird'></td> \
                </tr>";
                document.getElementById('tempTable').innerHTML += modalTemplate;
                document.getElementById('modalFirst').innerText = attacks[x]['datetime'];
                document.getElementById('modalSecond').innerText = attacks[x]['address'];
                document.getElementById('modalThird').innerText = attacks[x]['entered_pass'];
                document.getElementById('modalFirst').removeAttribute('id');
                document.getElementById('modalSecond').removeAttribute('id');
                document.getElementById('modalThird').removeAttribute('id');
            };
            document.getElementById('tempTable').removeAttribute('id');
            document.getElementById('firstTemp').removeAttribute('id');
            document.getElementById('secondTemp').removeAttribute('id');
            document.getElementById('thirdTemp').removeAttribute('id');
            document.getElementById('fourthTemp').removeAttribute('id');
            document.getElementById('tempBtn').removeAttribute('id');
        };
        jsonPM = data;
    };
};