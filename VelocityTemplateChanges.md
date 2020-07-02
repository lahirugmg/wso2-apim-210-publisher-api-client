# Timeout, suspend, and retry configurations

```

        #macro ( timeout $config)
            #if( $config.get("actionSelect") == "neverTimeout" )
            ## print nothing.
            #elseif($config.get("actionDuration")|| $config.get("actionSelect"))
            <timeout>
            #print_if_exist_only("duration" $config.get("actionDuration"))
            #print_if_exist_only("responseAction" $config.get("actionSelect"))
            </timeout>
           #else
               ##add default timeout config
            <timeout>
                <duration>1500</duration>
                <responseAction>fault</responseAction>
            </timeout>
            #end
            #if($config.get("suspendErrorCode")|| $config.get("suspendDuration")|| $config.get("suspendMaxDuration")|| $config.get("factor"))
            <suspendOnFailure>
                #print_list( "errorCodes" $config.get("suspendErrorCode"))
                #print_if_exist_only("initialDuration" $config.get("suspendDuration"))
                #print_if_exist_only("maximumDuration" $config.get("suspendMaxDuration"))
                <progressionFactor>#print_if_exist( $config.get("factor") 1.0)</progressionFactor>
            </suspendOnFailure>
            #else
            <suspendOnFailure>
               <initialDuration>1000</initialDuration>
               <progressionFactor>2.0</progressionFactor>
               <maximumDuration>5000</maximumDuration>
            </suspendOnFailure>
            #end
            #if($config.get("retryErroCode")|| $config.get("retryTimeOut")|| $config.get("retryDelay"))
            <markForSuspension>
                #print_list("errorCodes" $config.get("retryErroCode"))
                <retriesBeforeSuspension>#print_if_exist( $config.get("retryTimeOut") 0)</retriesBeforeSuspension>
                <retryDelay>#print_if_exist( $config.get("retryDelay") 0)</retryDelay>
            </markForSuspension>
            #else
            <markForSuspension>
               <errorCodes>101504,101505</errorCodes>
               <retriesBeforeSuspension>3</retriesBeforeSuspension>
               <retryDelay>3000</retryDelay>
            </markForSuspension>
            #end
        #end

```

