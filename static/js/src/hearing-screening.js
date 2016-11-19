var stimuli = [{'filename': 'tones2_0.wav', 'num_tones': 2},
		   {'filename': 'tones2_1.wav', 'num_tones': 2},
		   {'filename': 'tones2_2.wav', 'num_tones': 2},
		   {'filename': 'tones2_3.wav', 'num_tones': 2},
		   {'filename': 'tones3_0.wav', 'num_tones': 3},
		   {'filename': 'tones3_1.wav', 'num_tones': 3},
		   {'filename': 'tones3_2.wav', 'num_tones': 3},
		   {'filename': 'tones3_3.wav', 'num_tones': 3},
		   {'filename': 'tones4_0.wav', 'num_tones': 4},
		   {'filename': 'tones4_1.wav', 'num_tones': 4},
		   {'filename': 'tones4_2.wav', 'num_tones': 4},
		   {'filename': 'tones4_3.wav', 'num_tones': 4},
		   {'filename': 'tones5_0.wav', 'num_tones': 5},
		   {'filename': 'tones5_1.wav', 'num_tones': 5},
		   {'filename': 'tones5_2.wav', 'num_tones': 5},
		   {'filename': 'tones5_3.wav', 'num_tones': 5},
		   {'filename': 'tones6_0.wav', 'num_tones': 6},
		   {'filename': 'tones6_1.wav', 'num_tones': 6},
		   {'filename': 'tones6_2.wav', 'num_tones': 6},
		   {'filename': 'tones6_3.wav', 'num_tones': 6},
		   {'filename': 'tones7_0.wav', 'num_tones': 7},
		   {'filename': 'tones7_1.wav', 'num_tones': 7},
		   {'filename': 'tones7_2.wav', 'num_tones': 7},
		   {'filename': 'tones7_3.wav', 'num_tones': 7},
		   {'filename': 'tones8_0.wav', 'num_tones': 8},
		   {'filename': 'tones8_1.wav', 'num_tones': 8},
		   {'filename': 'tones8_2.wav', 'num_tones': 8},
		   {'filename': 'tones8_3.wav', 'num_tones': 8}];

function HearingScreening() {
	this.audio1Idx = -1;
	this.audio2Idx = -1;
	this.inputCode = 53;
}

HearingScreening.prototype.initialize = function () {
	this.genStimulusIdxs();

    var audio1element = new Audio();

    // set attributes
    audio1element.src = 'static/wav/' + stimuli[this.audio1Idx].filename;
    audio1element.controls = true;
    audio1element.id = 'audio1';
	$('#audio1-container').append(audio1element);

    var audio2element = new Audio();

    // set attributes
    audio2element.src = 'static/wav/' + stimuli[this.audio2Idx].filename;
    audio2element.controls = true;
    audio2element.id = 'audio2';
	$('#audio2-container').append(audio2element);

	var handle = this;
	$("#hearing-test-form").submit(function( event ) {
		handle.evaluate(parseInt($('#audiofile1-tone-count').val()), parseInt($('#audiofile2-tone-count').val()));
		event.preventDefault();
	});
};

HearingScreening.prototype.evaluate = function (count1, count2) {
	var returnCode;
	if ((count1===stimuli[this.audio1Idx].num_tones) && (count2===stimuli[this.audio2Idx].num_tones)) {
		returnCode = md5("pass" + (this.inputCode * this.inputCode));
	} else {
		returnCode = md5("fail" + (this.inputCode * this.inputCode));
	}

	$('#completion-code').val(returnCode);
	$('#completion-modal').modal('open');
};

HearingScreening.prototype.genStimulusIdxs = function () {
	this.audio1Idx = Math.floor(Math.random() * stimuli.length);
	this.audio2Idx = Math.floor(Math.random() * stimuli.length);
	// make sure they are different
	while (this.audio1Idx===this.audio2Idx) {
		this.audio2Idx = Math.floor(Math.random() * stimuli.length);
	}
};