import argparse, logging, re
from googleapiclient.discoverty import build
from oauth2client.client import GoogleCredentials
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

def retrieve_job_id(element):
	project = 'project_id'
	job_prefix = 'myjob_prefix'
	# location = 'us-central1'
	logging.info('looking for job with prefix {}'.format(job_prefix))

	try:
		credentails = GoogleCredentials.get_application_default()
		dataflow = build('dataflow', 'v1b3', credentials = credentials)
		result = dataflow.projects().locations().jobs().list(projectId = project,
		                                                     location = location).execute()
		job_id = 'None'
		for job in result['jobs']:
			if re.findall(r''+re.escape(job_prefix) + '', job['name']):
				job_id = job['id']
				break

		logging.info("Job ID: {}".format(job_id))
		return job_id

	except Exception as e:
		logging.info('Error retrieving Job ID')
		raise KeyError(e)

def run(argv = None):
	parser = argparse.ArgumentParser()
	known_args, pipeline_args = parse.parse_known_args(argv)

	pipeline_options = PipelineOptions(pipeline_args)
	pipeline_options.view_as(SetupOptions).save_main_session = True

	p = beam.Pipeline(options = pipeline_options)
	init_data = (p
	             | 'Start' >> beam.Create(["init pipeline"])
	             | 'Retrieve Job ID' >> beam.FlatMap(retrieve_job_id))

	p.run()

if __name__ == '__main__':
	main()
	             	)