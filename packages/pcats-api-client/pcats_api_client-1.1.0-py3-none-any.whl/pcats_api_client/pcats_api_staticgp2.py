import requests
import sys
import time

def _url(path):
    return 'https://pcats.research.cchmc.org' + path

def job_status(jobid):
    """Return job status.

    Return status of the previously submitted job

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job

    Returns
    -------
    string
        status

    """

    if jobid is None:
        return "Error"
    res=requests.get(_url('/api/job/{}/status'.format(jobid)))
    if res.status_code==200:
        res_json = res.json()
        if 'status' in res_json:
            return res_json['status']
    return None

def ret_jobid(res):
    if res.status_code==200:
        res_json = res.json()
        if 'jobid' in res_json:
            return res_json['jobid']
    return None

def staticgp2(datafile=None,
             dataref=None,
             method="BART",
             outcome=None,
             outcome_type="Continuous", 
             outcome_bound_censor="neither",
             outcome_lb=None,
             outcome_ub=None,
             outcome_censor_yn=None,
             outcome_censor_lv=None,
             outcome_censor_uv=None,
             outcome_link="identity",
             treatment=None, 
             x_explanatory=None,
             x_confounding=None,
             tr_type="Discrete",
             tr2_type="Discrete",             
             tr_values=None,
             tr2_values=None,
             pr_values=None,
             tr_hte=None,
             tr2_hte=None,
             burn_num=500,
             mcmc_num=500,
             x_categorical=None,
             mi_datafile=None,
             mi_dataref=None,
             sheet=None,
             mi_sheet=None,
             seed=5000,
             token=None,
             use_cache=None,
             reuse_cached_jobid=None):
    """Performs a data analysis for data with non-adaptive treatment(s).

      Bayesian's Gaussian process regression or Bayesian additive regression tree for data with non-adaptive treatment(s).

    Parameters
    ----------
    datafile File to upload (.csv or .xls)
    dataref Reference to already uploaded file.
    method The method to be used. "GP" for GP method and "BART" for BART method. The default value is "BART".
    outcome The name of the outcome variable.
    outcome.type Outcome type ("Continuous" or "Discrete"). The default value is "Continuous".
    outcome.bound_censor The default value is "neither".
          "neither" if the outcome is not bounded or censored.
          "bounded" if the outcome is bounded.
          "censored" if the outcome is censored.
    outcome.lb Putting a lower bound if the outcome is bounded.
    outcome.ub Putting a upper bound if the outcome is bounded.
    outcome.censor.yn Censoring variable if outcome is censored.
    outcome.censor.lv lower variable of censored interval if outcome is censored.
    outcome.censor.uv upper variable of censored interval if outcome is censored.
    outcome.link function for outcome; the default value is "identity".
          "identity" if no transformation needed.
          "log" for log transformation.
          "logit" for logit transformation.
    treatment The vector of the name of the treatment variables. Users can input at most two treatment variables.
    x.explanatory The vector of the name of the explanatory variables.
    x.confounding The vector of the name of the confounding variables.
    tr.type The type of the first treatment. "Continuous" for continuous treatment and "Discrete" for categorical treatment. The default value is "Discrete".
    tr2.type The type of the second treatment if available. "Continuous" for continuous treatment and "Discrete" for categorical treatment. The default value is "Discrete".
    tr.values user-defined values for the calculation of ATE if the first treatment variable is continuous
    tr2.values user-defined values for the calculation of ATE if the second treatment variable is continuous
    pr.values An optional vector of user-defined values of c for PrTE.
    tr.hte An optional vector specifying variables which may have heterogeneous treatment effect with the first treatment variable
    tr2.hte An optional vector specifying variables which may have heterogeneous treatment effect with the second treatment variable
    burn.num numeric; the number of MCMC 'burn-in' samples, i.e. number of MCMC to be discarded. The default value is 500.
    mcmc.num numeric; the number of MCMC samples after 'burn-in'. The default value is 500.
    x.categorical A vector of the name of categorical variables in data.
    mi.datafile File to upload (.csv or .xls) that contains the imputed data in the model.
    mi.dataref Reference to already uploaded file that contains the imputed data in the model.
    sheet If \code{datafile} or \code{dataref} points to an Excel file this variable specifies which sheet to load.
    mi.sheet If \code{mi.datafile} or \code{mi.dataurl} points to an Excel file this variable specifies which sheet to load.
    seed Sets the seed. The default value is 5000.
    token Authentication token.
    use_cache Use cached results (default True).

    Returns
    -------
    UUID
        jobid
    """

    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        'dataref': (None, dataref),
        'outcome': (None, outcome),
        'treatment': (None, treatment),
        'x.explanatory': (None, x_explanatory),
        'x.confounding': (None, x_confounding),
        'tr.hte': (None, tr_hte),
        'tr2.values': (None, tr2_values),
        'burn.num': (None, burn_num),
        'mcmc.num': (None, mcmc_num),
        'outcome.lb': (None, outcome_lb),
        'outcome.ub': (None, outcome_ub),
        'outcome.bound_censor': (None, outcome_bound_censor),
        'outcome.type': (None, outcome_type),
        'outcome.censor.lv': (None, outcome_censor_lv),
        'outcome.censor.uv': (None, outcome_censor_uv),
        'outcome.censor.yn': (None, outcome_censor_yn),
        'outcome.link': (None, outcome_link),
        'tr.type': (None, tr_type),
        'tr2.type': (None, tr2_type),
        'tr.values': (None, tr_values),
        'tr2.values': (None, tr2_values),
        'pr.values': (None, pr_values),
        'x.categorical': (None, x_categorical),
        'method': (None, method),
        'mi.data':  (mi_datafile, open(mi_datafile, 'rb')
                     if mi_datafile!=None else None ),
        'mi.dataref': (None, mi_dataref),
        'sheet': (None, sheet),
        'mi.sheet': (None, mi_sheet),
        'seed': (None, seed)
        }

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    elif (str(use_cache)=="0"):
        headers["X-API-Cache"]="0"

    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"
    elif (str(reuse_cached_jobid)=="0"):
        headers["X-API-Reuse-Cached-Jobid"]="0"

    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    res=requests.post(_url('/api/staticgp2'), files=data, headers=headers);
    return ret_jobid(res)

