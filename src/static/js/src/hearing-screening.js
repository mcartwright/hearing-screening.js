function HearingScreening(inputCode) {
	this.audio1Idx = -1;
	this.audio2Idx = -1;
	this.inputCode = inputCode;
}

HearingScreening.prototype.initialize = function () {
	this.genStimulusIdxs();

    var audio1element = new Audio();

    // set attributes
    audio1element.src = 'static/audio/' + stimuli[this.audio1Idx].filename;
    audio1element.controls = true;
    audio1element.id = 'audio1';
	$('#audio1-container').append(audio1element);

    var audio2element = new Audio();

    // set attributes
    audio2element.src = 'static/audio/' + stimuli[this.audio2Idx].filename;
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